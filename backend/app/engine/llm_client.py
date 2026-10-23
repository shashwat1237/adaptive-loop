import json
import logging
import time
import httpx
from typing import Dict, Any, Tuple
from app.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self.temperature = settings.LLM_TEMPERATURE
        self.provider = settings.LLM_PROVIDER
        self.fallback_to_mock = settings.FALLBACK_TO_MOCK
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    def call_chat_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        member_id: str,
        stage: str  # "analyst" or "critic"
    ) -> Dict[str, Any]:
        """Calls Groq API with JSON object formatting, with strict error propagation and no silent mocks."""
        if self.provider == "mock":
            logger.info(f"Running in explicit test mock mode for member {member_id} (stage: {stage})")
            return self._get_mock_response(member_id, stage)

        if self.provider != "groq":
            raise RuntimeError(f"Unsupported LLM provider '{self.provider}'. Only 'groq' is supported for live production inference.")

        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY is missing. Production live inference requires a valid Groq API key.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Adaptive-Loop/1.0.0"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": self.temperature,
            "max_tokens": 1400
        }

        max_retries = 5
        last_error = "Unknown error"
        for attempt in range(max_retries):
            try:
                with httpx.Client(timeout=35.0) as client:
                    response = client.post(self.base_url, headers=headers, json=payload)
                    if response.status_code == 200:
                        content = response.json()["choices"][0]["message"]["content"]
                        return json.loads(content)
                    elif response.status_code == 429:
                        last_error = f"HTTP 429 Rate Limit: {response.text}"
                        wait_time = 7.0 + (attempt * 3.0)
                        logger.warning(
                            f"Groq TPM rate limit hit (attempt {attempt + 1}/{max_retries}). Waiting {wait_time:.1f}s before retrying..."
                        )
                        time.sleep(wait_time)
                        continue
                    else:
                        last_error = f"HTTP {response.status_code}: {response.text}"
                        logger.warning(
                            f"Groq API returned HTTP {response.status_code} (attempt {attempt + 1}): {response.text}"
                        )
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Groq API attempt {attempt + 1} failed: {e}")

            time.sleep(1.0 * (2 ** attempt))

        # Algorithmic honesty: Never silently fake an analysis
        if not self.fallback_to_mock:
            raise RuntimeError(f"Groq LLM call to '{self.model}' failed after {max_retries} attempts. Cause: {last_error}")

        logger.warning(f"FALLBACK_TO_MOCK active: serving mock response for member {member_id} (stage: {stage})")
        return self._get_mock_response(member_id, stage)

    def _get_mock_response(self, member_id: str, stage: str) -> Dict[str, Any]:
        """Deterministic mock responses corresponding to synthetic personas."""
        if stage == "analyst":
            if member_id == "MEM-1001":
                return {
                    "primary_hypothesis": {
                        "statement": "Zone 2 aerobic base conditioning and Citrus Bergamot supplementation significantly reduced ApoB and systemic inflammation markers.",
                        "confidence": "HIGH",
                        "cited_observations": ["OBS-BIO-APOB-D180", "OBS-BIO-CRP-D180", "OBS-WEAR-HRV-W24"]
                    },
                    "competing_hypotheses": [
                        {
                            "statement": "Dietary adjustments and consistent exercise volume independently improved hepatic lipid metabolism and autonomic recovery.",
                            "confidence": "MODERATE",
                            "cited_observations": ["OBS-BIO-LDL-D180", "OBS-WEAR-RHR-W24"]
                        }
                    ],
                    "unresolved_uncertainties": [
                        "Differentiating individual contribution of Citrus Bergamot vs. Zone 2 training volume without isolate testing."
                    ],
                    "initial_action_recommendation": "CONTINUE_PROTOCOL"
                }
            elif member_id == "MEM-1002":
                return {
                    "primary_hypothesis": {
                        "statement": "Magnesium L-Threonate and screen-time restriction improved deep sleep architecture and lowered evening hyperarousal.",
                        "confidence": "HIGH",
                        "cited_observations": ["OBS-BIO-CORT-D180", "OBS-WEAR-DEEP-W24"]
                    },
                    "competing_hypotheses": [
                        {
                            "statement": "Job resignation in Week 8 reduced allostatic load and psychological cortisol drivers.",
                            "confidence": "HIGH",
                            "cited_observations": ["CONF-CAREER-W08", "OBS-WEAR-HRV-W09"]
                        }
                    ],
                    "unresolved_uncertainties": [
                        "Inability to differentiate physiological impact of supplement from significant lifestyle load reduction."
                    ],
                    "initial_action_recommendation": "CONTINUE_PROTOCOL"
                }
            elif member_id == "MEM-1003":
                return {
                    "primary_hypothesis": {
                        "statement": "Berberine protocol showed negligible impact on HbA1c and fasting insulin primarily due to low protocol adherence and frequent travel disruption.",
                        "confidence": "HIGH",
                        "cited_observations": ["OBS-BIO-HBA1C-D180", "CONF-TRAVEL-W11", "CONF-TRAVEL-W20"]
                    },
                    "competing_hypotheses": [
                        {
                            "statement": "Baseline insulin resistance requires longer therapeutic duration or higher dosage once adherence barriers are addressed.",
                            "confidence": "MODERATE",
                            "cited_observations": ["OBS-BIO-INS-D180"]
                        }
                    ],
                    "unresolved_uncertainties": [
                        "Whether glycemic resistance would improve under compliant daily dosing."
                    ],
                    "initial_action_recommendation": "ABSTAIN_MORE_DATA_REQUIRED"
                }
            else:
                return {
                    "primary_hypothesis": {
                        "statement": "Observed longitudinal biomarker shifts correlate with prescribed lifestyle intervention.",
                        "confidence": "MODERATE",
                        "cited_observations": []
                    },
                    "competing_hypotheses": [],
                    "unresolved_uncertainties": ["Limited longitudinal observation history."],
                    "initial_action_recommendation": "EXTEND_OBSERVATION"
                }

        elif stage == "critic":
            if member_id == "MEM-1001":
                return {
                    "verdict": "APPROVED",
                    "critique": "The analyst correctly grounded findings in lab deltas and wearable recovery trends. High protocol adherence (88.3%) and absence of confounders support continuing protocol.",
                    "identified_cognitive_biases": [],
                    "overruled_action": None,
                    "action_rationale": "High compliance and significant ApoB reduction (-20.34%) justify protocol continuation as prescribed."
                }
            elif member_id == "MEM-1002":
                return {
                    "verdict": "AMENDED",
                    "critique": "Analyst's initial recommendation to CONTINUE_PROTOCOL overweights supplement efficacy and ignores that the career transition in Week 8 coincided exactly with the sustained deep sleep recovery inflection point.",
                    "identified_cognitive_biases": [
                        "Attribution Fallacy: assigning physiological recovery solely to the prescribed protocol."
                    ],
                    "overruled_action": "ADJUST_WITH_CLINICIAN",
                    "action_rationale": "Protocol may be continued, but clinician must account for reduced life stress before assuming magnesium was the sole curative agent."
                }
            elif member_id == "MEM-1003":
                return {
                    "verdict": "APPROVED",
                    "critique": "The analyst properly recognized that biomarker stability (HbA1c 5.9%) was caused by low protocol adherence (27.8%) rather than biochemical inefficacy.",
                    "identified_cognitive_biases": [],
                    "overruled_action": None,
                    "action_rationale": "Address behavioral barriers and travel schedules before altering clinical protocol."
                }
            else:
                return {
                    "verdict": "APPROVED",
                    "critique": "Standard baseline verification passed.",
                    "identified_cognitive_biases": [],
                    "overruled_action": None,
                    "action_rationale": "Extend observation window for additional wearable data."
                }


llm_client = LLMClient()
