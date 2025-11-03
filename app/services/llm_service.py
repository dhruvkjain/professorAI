import dspy
from typing import List, Dict
from app.models.syllabus_models import (
    SyllabusItem, 
    ChapterQA,  
    AnimationScript,
)
from app.models.manim_models import ImprovementResult
from app.utils.code_parser import extract_code_blocks

# dspy signatures
class SyllabusExtractionSignature(dspy.Signature):
    """
    Extract structured syllabus information from raw unstructured syllabus text.
    Produces a list of `SyllabusItem` objects capturing each unit and chapter with content, competencies, and explanation.
    """
    text: str = dspy.InputField(
        desc=(
            "The complete unstructured syllabus text."
            "It may include chapters, units, learning outcomes, competencies, subtopics, and brief descriptions."
            "Provide full text input (not summaries) to allow complete parsing of structure."
        )
    )
    syllabus: List[SyllabusItem] = dspy.OutputField(
        desc=(
            "A list of structured `SyllabusItem` objects, each containing:\n"
            "- `unit_title`: The name of the unit or module.\n"
            "- `unit_number`: The number or index of the unit (e.g., 'Unit I', 'Unit II').\n"
            "- `chapter`: The chapter title under the unit.\n"
            "- `content`: A detailed list of core topics and subtopics in this chapter.\n"
            "- `competencies`: A list of learning goals or skills expected from this chapter.\n"
            "- `explanation`: A short summary or conceptual overview of the chapter.\n"
        )
    )

class ChapterDependencySignature(dspy.Signature):
    """
    Identify prerequisite (dependent) chapters for a given chapter in the syllabus.
    """
    chapter: str = dspy.InputField(
        desc=(
            "The exact chapter title whose dependencies are to be identified. "
            "Provide the same title string as in the syllabus for best matching."
        )
    )
    chapter_list: List[str] = dspy.InputField(
        desc=(
            "A list of all available chapter titles (strings) in the syllabus, "
            "used as the possible dependency pool."
        )
    )
    dependencies: List[str] = dspy.OutputField(
        desc=(
            "A list of chapter titles (strings) that are prerequisites for the given chapter. "
        )
    )

class QAGenerationSignature(dspy.Signature):
    """
    Generate concept-focused question–answer pairs for a given chapter based on its syllabus item.
    """
    item: SyllabusItem = dspy.InputField(
        desc=(
            "A fully structured `SyllabusItem` object containing:\n"
            "- `unit_title`: The unit name.\n"
            "- `unit_number`: The unit number.\n"
            "- `chapter`: The specific chapter title.\n"
            "- `content`: The main topics and subtopics in the chapter.\n"
            "- `competencies`: Key learning objectives.\n"
            "- `explanation`: A brief conceptual overview.\n"
            "This input contains `content` and `competencies` that provides the context for generating relevant conceptual questions."
        )
    )
    qa: ChapterQA = dspy.OutputField(
        desc=(
            "A `ChapterQA` object containing:\n"
            "- `chapter`: The same chapter title.\n"
            "- `qa_pairs`: A list of 5 to 8 (as required by content and competencies) detailed `QuestionAnswerPair` objects, each with:\n"
            "   * `question`: A concept-testing question based on the chapter content.\n"
            "   * `answer`: A clear, explanatory answer that reinforces understanding."
        )
    )

class ScriptGenerationSignature(dspy.Signature):
    """
    Generate a complete 2–3 minute animation script for a mathematical explainer video
    in the style of 3Blue1Brown, based on the subject, topic, insight, and key concepts.
    """
    subject: str = dspy.InputField(
        desc=(
            "The broad subject or academic domain, e.g., 'Mathematics', 'Physics', or 'Computer Science'. "
            "Used to define the tone, level, and style of explanation."
        )
    )
    topic: str = dspy.InputField(
        desc=(
            "The specific topic or chapter being explained (e.g., 'Polynomials', 'Matrix Determinant'). "
            "Should match a chapter from the syllabus."
        )
    )
    brief_insight: str = dspy.InputField(
        desc=(
            "A short 1–2 sentence conceptual summary that captures the central idea or insight of the topic. "
            "For example: 'A polynomial can approximate smooth curves with surprising precision.'"
        )
    )
    key_concepts: List[str] = dspy.InputField(
        desc=(
            "A list of subtopics or core ideas that should appear in the video, "
            "such as ['Roots of equations', 'Graph interpretation', 'Factorization', 'Real vs complex roots']."
        )
    )
    script: AnimationScript = dspy.OutputField(
        desc=(
            "An `AnimationScript` object containing:\n"
            "- `title`: The final video title (same as topic).\n"
            "- `narration`: The full narration text timed for 2–3 minutes of speech.\n"
            "- `visual_elements`: A list of `VisualElement` items, each with:\n"
            "    * `timestamp`: A timestamp (e.g., '00:10').\n"
            "    * `description`: A short visual cue, like 'Show parabola opening upward'.\n"
            "- `equations`: A list of equations displayed during the video.\n"
            "- `key_timestamps`: A mapping of labeled transitions (e.g., {'Intro': '00:00', 'Key insight': '01:15'}).\n"
            "- `visual_style`: A short description of the artistic tone, e.g., 'minimal vector style'."
        )
    )

class ManimGenerationSignature(dspy.Signature):
    """
    Generate a short (30–60 second), fully functional Manim animation script 
    visually explaining a mathematical concept using simple, clean visuals.
    """
    subject: str = dspy.InputField(
        desc=(
            "The broad academic subject, e.g., 'Mathematics', 'Physics', or 'Computer Science'. "
            "This determines notation, symbolism, and tone of narration."
        )
    )
    topic: str = dspy.InputField(
        desc=(
            "The syllabus topic or chapter this animation belongs to, e.g., 'Geometry', 'Trigonometry', or 'Calculus'."
        )
    )
    title: str = dspy.InputField(
        desc=(
            "The precise concept title to visualize, e.g., 'Pythagoras Theorem', 'Derivative as Slope'. "
            "Used as the animation’s main heading and the class name in Manim."
        )
    )
    narration: str = dspy.InputField(
        desc=(
            "The full narration text synchronized with visuals, long enough for a 30–60 second voiceover. "
            "Should describe the concept clearly while guiding the viewer through each visual transition."
        )
    )
    visual_elements: List[str] = dspy.InputField(
        desc=(
            "A list of key visual cues, each describing what appears and when. "
            "Each element should include both timing and action, e.g., "
            "'00:05 – Display right triangle', '00:15 – Highlight hypotenuse', '00:30 – Fade in equation'."
        )
    )
    equations: List[str] = dspy.InputField(
        desc=(
            "A list (1–2 items) of mathematical equations to render and animate using Manim’s `MathTex`. "
            "Example: ['a^2 + b^2 = c^2']."
        )
    )
    key_timestamps: Dict[str, str] = dspy.InputField(
        desc=(
            "A mapping of key labeled moments in the video (e.g., 'Introduction', 'Equation reveal') "
            "to their timestamps in 'mm:ss' format. "
            "Used to structure the animation sequence."
        )
    )
    visual_style: str = dspy.InputField(
        desc=(
            "A short text describing the overall tone or look of the visuals, e.g., "
            "'minimal whiteboard style', '3Blue1Brown-inspired gradient animation', or 'flat geometry style'."
        )
    )
    manim_code: str = dspy.OutputField(
        desc=(
            "A complete and verified Python script enclosed in ```python``` fences. The script **must**:\n"
            "1. Be fully compatible with **Manim Community v0.18+**.\n"
            "2. Include a valid Scene class inheriting from `Scene`.\n"
            "3. Use only supported imports: `from manim import *`.\n"
            "4. Contain 2–3 sequential animations using **official v0.18+ APIs** like `Write`, `Create`, `FadeIn`, `Transform`.\n"
            "5. Render at most 1–2 `MathTex` equations.\n"
            "6. Include inline comments explaining each visual action.\n"
            "7. Save the rendered video as `video.mp4`.\n\n"
            "**Validation Requirement:**\n"
            "- The code must avoid deprecated classes functions etc (e.g., `ShowCreation`, `FadeOutAndShiftDown`).\n"
            "- All parameters (like `run_time`, `shift`, `scale`) must match current Manim function signatures.\n"
            "- Generated output should pass syntax validation for Manim v0.18+ before execution."
        )
    )

class ImprovementSignature(dspy.Signature):
    """
    Given a Manim Python script, its execution logs, and any errors produced,
    along with optional base64-encoded video frames (if available),
    suggest an improved version of the script that fixes the issues and
    enhances the animation quality.

    The improved code must be returned **inside a Python code block**.
    """
    executed_code = dspy.InputField(desc="The Manim Python source code that was executed.")
    logs = dspy.InputField(desc="The stdout logs captured from the execution.")
    errors = dspy.InputField(desc="The stderr or error tracebacks captured from the execution.")
    base64_frames = dspy.InputField(desc="List of base64-encoded video frames (subset or empty).")

    improved_code = dspy.OutputField(desc="The improved Manim Python code, inside a ```python ... ``` code block.")


# dspy modules
class SyllabusExtractor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(SyllabusExtractionSignature)

    def forward(self, text):
        result = self.predict(text=text)
        return result.syllabus

class ChapterDependencyFinder(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(ChapterDependencySignature)

    def forward(self, chapter, chapter_list):
        result = self.predict(chapter=chapter, chapter_list=chapter_list)
        return result.dependencies

class QAGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(QAGenerationSignature)

    def forward(self, item: SyllabusItem) -> ChapterQA:
        result = self.predict(item=item)
        return result.qa

class ScriptGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(ScriptGenerationSignature)

    def forward(self, subject: str, item: SyllabusItem) -> AnimationScript:
        topic = item.chapter
        brief_insight = item.explanation
        key_concepts = item.content

        result = self.predict(
            subject=subject,
            topic=topic,
            brief_insight=brief_insight,
            key_concepts=key_concepts
        )
        return result.script

class ManimGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(ManimGenerationSignature)

    def forward(self, subject: str, topic: str, script: AnimationScript) -> str:
        visual_elements_text = [
            f"{elem.timestamp}: {elem.description}" for elem in script.visual_elements
        ]

        equations_text = script.equations
        timestamps = script.key_timestamps

        result = self.predict(
            subject=subject,
            topic=topic,
            title=script.title,
            narration=script.narration,
            visual_elements=visual_elements_text,
            equations=equations_text,
            key_timestamps=timestamps,
            visual_style=script.visual_style,
        )

        return result.manim_code

class ImproveCodeOnce(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predict = dspy.Predict(ImprovementSignature)

    def forward(self, executed_code: str, logs: str, errors: str, base64_frames: list[str]) -> ImprovementResult:
        # avoid sending large base64 blobs just send a summary
        frame_summary = f"{len(base64_frames)} frames provided." if base64_frames else "No frames provided."

        result = self.predict(
            executed_code=executed_code,
            logs=logs,
            errors=errors,
            base64_frames=frame_summary,
        )

        if isinstance(result, str):
            improved_code = extract_code_blocks(result).get("python", result)
        else:
            improved_code = extract_code_blocks(
                getattr(result, "improved_code", "")
            ).get("python", getattr(result, "improved_code", ""))

        return ImprovementResult(improved_code=improved_code)