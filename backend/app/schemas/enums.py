from enum import Enum


class BiologicalSexEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class ProtocolCategoryEnum(str, Enum):
    LIFESTYLE = "LIFESTYLE"
    SUPPLEMENT = "SUPPLEMENT"
    EXERCISE = "EXERCISE"
    NUTRITION = "NUTRITION"


class ConfounderEventTypeEnum(str, Enum):
    ILLNESS = "ILLNESS"
    TRAVEL = "TRAVEL"
    LIFE_STRESS = "LIFE_STRESS"
    INJURY = "INJURY"


class ConfounderSeverityEnum(str, Enum):
    MILD = "MILD"
    MODERATE = "MODERATE"
    SEVERE = "SEVERE"


class AnalysisStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ABSTAINED = "ABSTAINED"


class ActionRecommendationEnum(str, Enum):
    CONTINUE_PROTOCOL = "CONTINUE_PROTOCOL"
    EXTEND_OBSERVATION = "EXTEND_OBSERVATION"
    ADJUST_WITH_CLINICIAN = "ADJUST_WITH_CLINICIAN"
    CLINICAL_ESCALATION = "CLINICAL_ESCALATION"
    ABSTAIN_MORE_DATA_REQUIRED = "ABSTAIN_MORE_DATA_REQUIRED"


class CriticVerdictEnum(str, Enum):
    APPROVED = "APPROVED"
    AMENDED = "AMENDED"
    REJECTED = "REJECTED"


class ConfidenceLevelEnum(str, Enum):
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    INCONCLUSIVE = "INCONCLUSIVE"
