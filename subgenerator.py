import os
import subprocess
from translate import Translator

input_file = "videos.txt"
language = "English"
translation_language = "es"
subtitles_dir = "sub"


def ensure_directory_exists(directory):
    """Crea el directorio si no existe."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def translate_subtitles(srt_file):
    """Traduce un archivo de subtítulos .srt al idioma especificado."""
    try:
        output_file = os.path.join(
            subtitles_dir, os.path.splitext(os.path.basename(srt_file))[0] + f"_{translation_language}.srt")
        translator = Translator(to_lang=translation_language)

        with open(srt_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
            for line in infile:
                if line.strip().isdigit() or "-->" in line:
                    outfile.write(line)
                else:
                    translated_text = translator.translate(line.strip())
                    outfile.write(translated_text + "\n")

        print(f"Subtítulos traducidos guardados en: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error al traducir el archivo .srt: {e}")
        return None


def generate_subtitles(video_path):
    """Genera subtítulos para un video usando Whisper."""
    try:
        print(f"Generando subtítulos para: {video_path}")
        subprocess.run(
            ["whisper", video_path, "--language", language], check=True)

        srt_file = os.path.join(
            subtitles_dir, os.path.splitext(os.path.basename(video_path))[0] + ".srt")
        original_srt_file = os.path.splitext(
            os.path.basename(video_path))[0] + ".srt"

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
        output_path = os.path.join(video_dir, f"sub-{video_name}")

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
    ensure_directory_exists(subtitles_dir)

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
                translated_srt_file = translate_subtitles(srt_file)
                if translated_srt_file:
                    embed_subtitles(video_path, translated_srt_file)
        else:
            print(f"Error: El archivo {video_path} no existe.")


if __name__ == "__main__":
    main()
