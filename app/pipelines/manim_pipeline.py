import os, dspy, asyncio
from datetime import datetime
from pathlib import Path

from app.models.syllabus_models import AnimationScript
from app.services.llm_service import (
    ManimGenerator,
    ImproveCodeOnce,
)
from app.services.manim_services import (
    get_frames_from_video,
    execute_manim,
)
from app.utils.code_parser import extract_code_blocks 
from app.config.config import OPEN_AI_API_KEY


def get_manim_video_path(code_file: str, quality: str = "1080p60") -> Path:
    script_stem = Path(code_file).stem
    video_dir = Path(code_file).parent / "media" / "videos" / script_stem / quality
    return video_dir / f"{script_stem}.mp4"

async def process_single_manim_file(
    subject: str,
    chapter: str,
    script_model: AnimationScript,
    output_dir: str,
    iterations: int = 3,
):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    chapter_name = chapter.replace(" ", "_")
    file_path = os.path.join(output_dir, f"{chapter_name}_manim_{timestamp}.py")

    # generate initial manim code
    manim_gen = ManimGenerator()
    manim_code = manim_gen(subject, chapter, script_model)

    executed_code = extract_code_blocks(manim_code)["python"]
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(executed_code)

    video_path = get_manim_video_path(file_path)

    improver = ImproveCodeOnce()

    # iterative improvement loop
    i = 0
    logs, errors = "", ""

    while i < iterations:
        print(f"[Iteration {i+1}/{iterations}] Executing {file_path}...")
        result = execute_manim(file_path)

        if result["stdout"]:
            print("=== LOGS ===")
            print(result["stdout"])

        if result["stderr"]:
            print("=== ERRORS ===")
            print(result["stderr"])

        if result["returncode"] != 0:
            print(f"Command failed with exit code {result["returncode"]}")
        else:
            print(f"Execution succeeded on iteration {i+1}")
            break

        logs, errors = result["stdout"], result["stderr"]
        print(f"Errors detected on iteration {i+1}, invoking improver...")

        # try to extract video frames if a partial render exists
        try:
            base64_frames = get_frames_from_video(str(video_path))
        except Exception:
            base64_frames = []

        # run dspy model to improve the code
        improvement_result: ImprovementResult = improver(
            executed_code=executed_code,
            logs=logs,
            errors=errors,
            base64_frames=base64_frames,
        )

        executed_code = improvement_result.improved_code

        # save the improved code
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(executed_code)

        print(f"Applied improvement on iteration {i+1}")

        i += 1

    print(f"[Final Status] {'Success...' if not errors.strip() else 'Failed after retries...'}")

    return {
        "file": file_path,
        "iterations": i,
        "success": not bool(errors.strip()),
        "logs": logs[-2000:],   # keep last few KB for trace
        "errors": errors[-2000:] if errors else "",
    }

def process_manim_script_pipeline(subject: str, syllabus_data: list[dict]):
    # configuration of openai in dspy
    openai_lm = dspy.LM(
        model="openai/gpt-5",
        api_key=OPEN_AI_API_KEY,
        temperature=1.0,
        max_tokens=16000,
    )

    os.makedirs("test_doc", exist_ok=True)
    results = []

    with dspy.context(lm=openai_lm):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        for item in syllabus_data:
            if not item.get("animation"):
                continue

            script_model = AnimationScript(**item["animation"])
            chapter = item["chapter"]

            # run each item synchronously in this background thread
            result = loop.run_until_complete(
                process_single_manim_file(
                    subject=subject,
                    chapter=chapter,
                    script_model=script_model,
                    output_dir="test_doc",
                    iterations=3,
                )
            )
            results.append(result)

        loop.close()

    return results
