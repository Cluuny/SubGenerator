import os
import subprocess

# Ruta al archivo que contiene las rutas de los videos
input_file = "videos.txt"
language = "English"  # Idioma para los subtítulos


def generate_subtitles(video_path):
    """Genera subtítulos para un video usando Whisper."""
    try:
        print(f"Generando subtítulos para: {video_path}")
        subprocess.run(
            ["whisper", video_path, "--language", language], check=True)
        # El archivo .srt se genera en la misma carpeta donde se ejecuta el script
        srt_file = os.path.join("./", os.path.splitext(
            os.path.basename(video_path))[0] + ".srt")
        print(srt_file)
        if os.path.exists(srt_file):
            return srt_file
        else:
            print(f"Error: No se generó el archivo .srt para {video_path}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error al generar subtítulos para {video_path}: {e}")
        return None


def embed_subtitles(video_path, srt_file):
    """Añade subtítulos al video usando ffmpeg."""
    try:
        video_dir = os.path.dirname(video_path)
        video_name = os.path.basename(video_path)
        output_path = os.path.join(video_dir, f"sub-{video_name}")

        # Convertir las rutas a formato absoluto y usar barras '/'
        video_path = os.path.abspath(video_path).replace("\\", "/")
        output_path = os.path.abspath(output_path).replace("\\", "/")

        print(f"Añadiendo subtítulos al video: {video_path}")
        subprocess.run([
            "ffmpeg", "-i", video_path, "-vf", f"subtitles='{
                srt_file}'", "-c:a", "copy", output_path
        ], check=True)
        print(f"Video con subtítulos guardado en: {output_path}")
        # Elimina el archivo .srt después de usarlo (opcional)
        os.remove(srt_file)
    except subprocess.CalledProcessError as e:
        print(f"Error al añadir subtítulos a {video_path}: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


def main():
    if not os.path.exists(input_file):
        print(f"Error: El archivo {input_file} no existe.")
        return

    with open(input_file, "r") as file:
        video_paths = file.readlines()

    for video_path in video_paths:
        video_path = video_path.strip()
        if os.path.exists(video_path):
            srt_file = generate_subtitles(video_path)
            if srt_file:
                embed_subtitles(video_path, srt_file)
        else:
            print(f"Error: El archivo {video_path} no existe.")


if __name__ == "__main__":
    main()
