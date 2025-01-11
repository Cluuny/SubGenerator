import os
import subprocess
from translate import Translator
import shutil

input_file = "videos.txt"
language = "English"
translation_language = "es"
subtitles_dir = "sub"


def ensure_directory_exists(directory):
    """Crea el directorio si no existe."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def clean_old_files(exclude_files):
    """
    Elimina la carpeta 'sub' y todos los archivos .json, .tsv, .srt, .vtt y .txt, 
    excepto los archivos especificados en exclude_files.
    """
    try:
        # Eliminar la carpeta 'sub' si existe
        if os.path.exists(subtitles_dir):
            shutil.rmtree(subtitles_dir)

        # Eliminar archivos en el directorio actual excepto los excluidos
        for file in os.listdir("."):
            if (file.endswith(('.json', '.tsv', '.srt', '.vtt', '.txt')) and
                    file not in exclude_files):
                os.remove(file)

        print("Archivos antiguos eliminados, excepto los especificados en la lista de exclusión.")
    except Exception as e:
        print(f"Error al limpiar los archivos antiguos: {e}")


def generate_subtitles(video_path):
    """Genera subtítulos para un video usando Whisper."""
    try:
        print(f"Generando subtítulos para: {video_path}")
        subprocess.run(
            ["whisper", video_path, "--language", language, "--output_format", "srt"], check=True)

        srt_file = os.path.join("./",
                                subtitles_dir, os.path.splitext(os.path.basename(video_path))[0] + ".srt")
        original_srt_file = os.path.splitext(
            os.path.basename(video_path))[0] + ".srt"

        print(original_srt_file)
        print(srt_file)

        # Mover el archivo generado a la carpeta de subtítulos
        if os.path.exists(original_srt_file):
            os.rename(original_srt_file, srt_file)
            return srt_file
        else:
            print(f"Error: No se generó el archivo .srt para {video_path}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error al generar subtítulos para {video_path}: {e}")
        return None


def embed_subtitles(video_path, srt_file):
    """Añade subtítulos al video usando ffmpeg con opciones de estilo."""
    try:
        video_dir = os.path.dirname(video_path)
        video_name = os.path.basename(video_path)
        base_name, ext = os.path.splitext(video_name)
        output_path = os.path.join(video_dir, f"{base_name}-sub{ext}")

        # Asegúrate de que las rutas estén correctamente formateadas
        video_path = os.path.abspath(video_path).replace("\\", "/")
        output_path = os.path.abspath(output_path).replace("\\", "/")

        print(f"Añadiendo subtítulos al video: {video_path}")

        subprocess.run([
            "ffmpeg", "-i", video_path, "-filter_complex",
            f"subtitles={
                srt_file}:force_style='BackColour=&HA0000000,BorderStyle=4,Fontsize=6'",
            "-c:a", "copy", output_path
        ], check=True)
        print(f"Video con subtítulos guardado en: {output_path}")
        os.remove(srt_file)
    except subprocess.CalledProcessError as e:
        print(f"Error al añadir subtítulos a {video_path}: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


def main():
    # Lista de archivos que deseas conservar
    exclude_files = [
        "requirements.txt",
        "videos.txt"
    ]

    # Limpiar archivos antiguos antes de comenzar
    clean_old_files(exclude_files)
    ensure_directory_exists(subtitles_dir)

    if not os.path.exists(input_file):
        print(f"Error: El archivo {input_file} no existe.")
        return

    with open(input_file, "r") as file:
        video_paths = file.readlines()

    for video_path in video_paths:
        video_path = video_path.strip()

        # Eliminar comillas si están presentes
        if video_path.startswith('"') and video_path.endswith('"'):
            video_path = video_path[1:-1]

        if os.path.exists(video_path):
            srt_file = generate_subtitles(video_path)
            if srt_file:
                print(srt_file)
                srt_file = srt_file.replace("\\", "/")
                embed_subtitles(video_path, srt_file)
        else:
            print(f"Error: El archivo {video_path} no existe.")


if __name__ == "__main__":
    main()
