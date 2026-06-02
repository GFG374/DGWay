import unittest
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import scan_available_models as scan


class ScanAvailableModelsTest(unittest.TestCase):
    def test_mask_secret_keeps_only_edges(self):
        masked = scan.mask_secret("sk-1234567890abcdef")
        self.assertEqual(masked, "sk-1...cdef")

    def test_candidate_set_dedupes_and_normalizes_gemini_names(self):
        candidates = scan.CandidateSet()
        candidates.add("gemini", "models/gemini-2.5-flash", "local")
        candidates.add("gemini", "gemini-2.5-flash", "live")
        candidates.add("openai", " gpt-image-2 ", "pricing")
        candidates.add("gemini", "geminiModels", "source-variable")
        candidates.add("antigravity", "claude-*", "wildcard")

        gemini = candidates.by_platform["gemini"]
        self.assertEqual(list(gemini), ["gemini-2.5-flash"])
        self.assertEqual(gemini["gemini-2.5-flash"].sources, ["local", "live"])
        self.assertIn("gpt-image-2", candidates.by_platform["openai"])
        self.assertNotIn("claude-*", candidates.by_platform["antigravity"])

    def test_classifies_required_capabilities(self):
        self.assertEqual(scan.classify_capability("openai", "gpt-image-2"), "image")
        self.assertEqual(scan.classify_capability("openai", "gpt-5.3-codex"), "codex")
        self.assertEqual(scan.classify_capability("gemini", "gemini-3.1-flash-image"), "gemini-image")
        self.assertEqual(scan.classify_capability("gemini", "gemini-2.5-flash"), "gemini-text")
        self.assertEqual(scan.classify_capability("antigravity", "claude-opus-4-8"), "claude-code")
        self.assertEqual(scan.classify_capability("antigravity", "gemini-3-pro-image"), "gemini-image")


if __name__ == "__main__":
    unittest.main()
