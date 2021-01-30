"""Defines the items related to player injuries."""
from enum import Enum, auto
import scrapy


class InjuryType(Enum):
    """The different reasons a player may appear on an injury report."""

    ABDOMEN = auto()
    ACHILLES = auto()
    ANKLE = auto()
    APPENDIX = auto()
    ARM = auto()
    ARRHYTHMIA = auto()
    BACK = auto()
    BICEPS = auto()
    BLOOD_CLOTS = auto()
    BLOOD_DISORDER = auto()
    C19 = auto()
    CALF = auto()
    CHEST = auto()
    CHIN = auto()
    CLAVICLE = auto()
    COACHS_DECISION = auto()
    COLLARBONE = auto()
    CONCUSSION = auto()
    CONDITIONING = auto()
    CORE_MUSCLE = auto()
    DEHYDRATION = auto()
    DENTAL = auto()
    DISCIPLINARY = auto()
    EAR = auto()
    ELBOW = auto()
    ELIGIBILITY = auto()
    EYE = auto()
    FACIAL = auto()
    FIBULA = auto()
    FINGER = auto()
    FOOT = auto()
    FOREARM = auto()
    GLUTE = auto()
    GROIN = auto()
    HAMSTRING = auto()
    HAND = auto()
    HEAD = auto()
    HEADACHES = auto()
    HEART = auto()
    HEAT = auto()
    HEAT_CRAMPS = auto()
    HEEL = auto()
    HERNIA = auto()
    HIP = auto()
    HIP_FLEXOR = auto()
    HOLDOUT = auto()
    ILLNESS = auto()
    JAW = auto()
    KIDNEY = auto()
    KNEE = auto()
    LEG = auto()
    LEGAL = auto()
    LIVER = auto()
    LOWER_LEG = auto()
    LUMBAR = auto()
    LUNG = auto()
    MCL = auto()
    MIGRAINES = auto()
    MOUTH = auto()
    NECK = auto()
    NOSE = auto()
    NOT_FOOTBALL_RELATED = auto()
    NOT_INJURY_RELATED = auto()
    OBLIQUE = auto()
    PECTORAL = auto()
    PELVIS = auto()
    PERSONAL = auto()
    QUADRICEPS = auto()
    REST = auto()
    RIBS = auto()
    SCAPULA = auto()
    SEIZURE = auto()
    SHIN = auto()
    SHORTNESS_OF_BREATH = auto()
    SHOULDER = auto()
    SOLARPLEXUS = auto()
    SPINE = auto()
    SPLEEN = auto()
    SPORTS_HERNIA = auto()
    STERNUM = auto()
    STINGER = auto()
    STOMACH = auto()
    SUSPENSION = auto()
    SUSPENSION_SERVED = auto()
    TAILBONE = auto()
    THIGH = auto()
    THROAT = auto()
    THUMB = auto()
    TIBIA = auto()
    TOE = auto()
    TORN_ACL = auto()
    TRAPEZIUS = auto()
    TRICEPS = auto()
    UNDISCLOSED = auto()
    UPPER_ARM = auto()
    UPPER_BODY = auto()
    WRIST = auto()


class InjuryStatus(Enum):
    """The different statuses that can show up on an injury report."""

    DOUBTFUL = auto()
    INJURED_RESERVE = auto()
    OUT = auto()
    PHYSICALLY_UNABLE_TO_PERFORM = auto()
    PROBABLE = auto()
    QUESTIONABLE = auto()
    SUSPENDED = auto()
    C19 = auto()
    RESERVE_OR_FUTURE = auto()
    INJURED_FROM_WAIVED = auto()


class InjuryOutcome(Enum):
    """Whether the player played or not."""

    DID_NOT_PLAY = auto()
    PLAYED = auto()


class Injury(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines an injury for a player in a specifc week of the season."""

    # A relative link on Pro Football Reference to the player.
    player = scrapy.Field()

    # A relative link on Pro Football Reference to the team the player was
    # playing for when the injury happened.
    team = scrapy.Field()

    # The week of the season the injury report was filed.
    week = scrapy.Field()

    # The status of the player listed on the injury report.
    status = scrapy.Field()

    # Whether the player played or not.
    outcome = scrapy.Field()

    @staticmethod
    def sql_create(database):
        """
        Creates the players table if one does not exist in the given database.
        Note that this does not update the fields if the table already exists,
        but the fields are outdated.
        """

        database.execute('''
            CREATE TABLE IF NOT EXISTS injuries (
                player TEXT,
                team TEXT,
                week INTEGER,
                status TEXT,
                outcome TEXT,
                PRIMARY KEY (player, team, week),
                FOREIGN KEY (player) REFERENCES players(player),
                FOREIGN KEY (team) REFERENCES teams(team)
            )
        ''')

    def sql_insert(self, database):
        """Insert this injury report into the injuries table."""

        database.execute(
            '''
            INSERT OR REPLACE INTO injuries (
                player,
                team,
                week,
                status,
                outcome
            ) VALUES (
                ?,
                ?,
                ?,
                ?,
                ?
            )
        ''', (self['player'], self['team'], self['week'], self['status'].name,
              self['outcome'].name))


class InjuryReason(scrapy.Item):  # pylint: disable=too-many-ancestors
    """Defines a reason that a player is missing for a week. There could be
    multiple reasons."""

    # A relative link on Pro Football Reference to the player.
    player = scrapy.Field()

    # A relative link on Pro Football Reference to the team the player was
    # playing for at the time of the injury.
    team = scrapy.Field()

    # The particular week of a season that this injury was listed. The same
    # injury may be listed for multiple weeks.
    week = scrapy.Field()

    # An instance of InjuryType
    reason = scrapy.Field()

    @staticmethod
    def sql_create(database):
        """
        Creates the injury_reasons table if one does not exist.

        The table is meant to contain the reasons that a player in the injuries
        table is appearning on the injury report. It is possible that there are
        multiple reasons which is why we are creating a separate table instead
        of another field in the injuries table.
        """

        database.execute('''
            CREATE TABLE IF NOT EXISTS injury_reasons (
                player TEXT,
                team TEXT,
                week INTEGER,
                reason TEXT,
                PRIMARY KEY (player, team, week),
                FOREIGN KEY (player) REFERENCES players(player),
                FOREIGN KEY (team) REFERENCES teams(team),
                FOREIGN KEY (player, team, week) 
                    REFERENCES injuries(player, team, week)
            )
        ''')

    def sql_insert(self, database):
        """Insert this injury reason into the injuries table."""

        database.execute(
            '''
            INSERT OR REPLACE INTO injury_reasons (
                player,
                team,
                week,
                reason
            ) VALUES (
                ?,
                ?,
                ?,
                ?
            )
        ''', (self['player'], self['team'], self['week'], self['reason'].name))


# Common typos and substitutions necessary to parse injury reasons from Pro
# Football Reference.
PFR_INJURY_REASON_SUBSTITUTIONS = {
    '': [InjuryType.UNDISCLOSED],
    '10_GAME_SUSPENSION_SERVED': [InjuryType.SUSPENSION_SERVED],
    'ABDOMDEN': [InjuryType.ABDOMEN],
    'ABDOMINA': [InjuryType.ABDOMEN],
    'ABDOMINAL': [InjuryType.ABDOMEN],
    'ABS': [InjuryType.CORE_MUSCLE],
    'ACHILLIES': [InjuryType.ACHILLES],
    'AHOULDER': [InjuryType.SHOULDER],
    'AMKLE': [InjuryType.ANKLE],
    'ANCHILLES': [InjuryType.ACHILLES],
    'ANKILE': [InjuryType.ANKLE],
    'ANKKLE': [InjuryType.ANKLE],
    'ANKLES': [InjuryType.ANKLE],
    'APPENDECTOMY': [InjuryType.APPENDIX],
    'ARCH': [InjuryType.FOOT],
    'BECK': [InjuryType.BACK],
    'BICEP': [InjuryType.BICEPS],
    'BILATERAL_GROIN': [InjuryType.GROIN],
    'BOTHKNEES': [InjuryType.KNEE],
    'BROKEN_FOOT': [InjuryType.FOOT],
    'BURNER': [InjuryType.STINGER],
    'BUTTOCKS': [InjuryType.GLUTE],
    'CONCUSISION': [InjuryType.CONCUSSION],
    'CONCUSSION_PROTOCOL': [InjuryType.CONCUSSION],
    'CORE': [InjuryType.CORE_MUSCLE],
    'COREMUSCLE': [InjuryType.CORE_MUSCLE],
    'DB': [InjuryType.SHOULDER],
    'DISLOCATED_WRIST': [InjuryType.WRIST],
    'EIGHT_GAME_SUSPENSION_SERVED': [InjuryType.SUSPENSION_SERVED],
    'EYELID': [InjuryType.EYE],
    'FACE': [InjuryType.FACIAL],
    'FACIALLACERATION': [InjuryType.FACIAL],
    'FACIAL_LACERATIONS': [InjuryType.FACIAL],
    'FEET': [InjuryType.FOOT],
    'FIVE_GAME_SUSPENSION_SERVED': [InjuryType.SUSPENSION_SERVED],
    'FLU': [InjuryType.ILLNESS],
    'FLU_LIKE_SYMPTOMS': [InjuryType.ILLNESS],
    'FOOT_SURGERY': [InjuryType.FOOT],
    'FOREAM': [InjuryType.FOREARM],
    'FOUR_GAME_SUSPENSION': [InjuryType.SUSPENSION],
    'FOUR_GAME_SUSPENSIONS_SERVED': [InjuryType.SUSPENSION_SERVED],
    'FOUR_GAME_SUSPENSION_SERVED': [InjuryType.SUSPENSION_SERVED],
    'FRACTURED_LEFT_FOOT': [InjuryType.FOOT],
    'FRACTURED_RIGHT_FOOT': [InjuryType.FOOT],
    'GENERAL_MEDICAL_ISSUE': [InjuryType.ILLNESS],
    'GLUTEUS': [InjuryType.GLUTE],
    'HAMSTING': [InjuryType.HAMSTRING],
    'HAMSTIRNG': [InjuryType.HAMSTRING],
    'HAMSTRINGS': [InjuryType.HAMSTRING],
    'HEADACHE': [InjuryType.HEADACHES],
    'HIIP': [InjuryType.HIP],
    'HIPS': [InjuryType.HIP],
    'HMASTRING': [InjuryType.HAMSTRING],
    'INFECTION': [InjuryType.ILLNESS],
    'KNE': [InjuryType.KNEE],
    'KNEES': [InjuryType.KNEE],
    'LEFTANKLE': [InjuryType.ANKLE],
    'LEFTCALF': [InjuryType.CALF],
    'LEFTELBOW': [InjuryType.ELBOW],
    'LEFTFINGER': [InjuryType.FINGER],
    'LEFTFOOT': [InjuryType.FOOT],
    'LEFTGROIN': [InjuryType.GROIN],
    'LEFTHAMSTRING': [InjuryType.HAMSTRING],
    'LEFTHAND': [InjuryType.HAND],
    'LEFTHIP': [InjuryType.HIP],
    'LEFTKNEE': [InjuryType.KNEE],
    'LEFTQUADRICEPS': [InjuryType.QUADRICEPS],
    'LEFTSHIN': [InjuryType.SHIN],
    'LEFTSHOULDER': [InjuryType.SHOULDER],
    'LEFTTHIGH': [InjuryType.THIGH],
    'LEFTTHUMB': [InjuryType.THUMB],
    'LEFTUPPERARM': [InjuryType.UPPER_ARM],
    'LEFTWRIST': [InjuryType.WRIST],
    'LEFT_ANKLE': [InjuryType.ANKLE],
    'LEFT_ARM': [InjuryType.ARM],
    'LEFT_BICEPS': [InjuryType.BICEPS],
    'LEFT_CALF': [InjuryType.CALF],
    'LEFT_ELBOW': [InjuryType.ELBOW],
    'LEFT_EYE': [InjuryType.EYE],
    'LEFT_FINGER': [InjuryType.FINGER],
    'LEFT_FOOT': [InjuryType.FOOT],
    'LEFT_FOREARM': [InjuryType.FOREARM],
    'LEFT_GROIN': [InjuryType.GROIN],
    'LEFT_HAMSTRING': [InjuryType.HAMSTRING],
    'LEFT_HAND': [InjuryType.HAND],
    'LEFT_HIP': [InjuryType.HIP],
    'LEFT_KNEE': [InjuryType.KNEE],
    'LEFT_LEG': [InjuryType.LEG],
    'LEFT_QUADRICEP': [InjuryType.QUADRICEPS],
    'LEFT_QUADRICEPS': [InjuryType.QUADRICEPS],
    'LEFT_SHIN': [InjuryType.SHIN],
    'LEFT_SHOULDER': [InjuryType.SHOULDER],
    'LEFT_THIGH': [InjuryType.THIGH],
    'LEFT_THUMB': [InjuryType.THUMB],
    'LEFT_TOE': [InjuryType.TOE],
    'LEFT_UPPER_ARM': [InjuryType.UPPER_ARM],
    'LEFT_WRIST': [InjuryType.WRIST],
    'LOWERLEG': [InjuryType.LOWER_LEG],
    'LOWER_BACK': [InjuryType.LUMBAR],
    'MEDICALILLNESS': [InjuryType.ILLNESS],
    'MIGRAINE': [InjuryType.MIGRAINES],
    'NACK': [InjuryType.NECK],
    'NINE_GAME_SUSPENSION_SERVED': [InjuryType.SUSPENSION_SERVED],
    'NON_FOOTBALL_ILLNESS': [InjuryType.ILLNESS],
    'NOTINJURYRELATED': [InjuryType.NOT_INJURY_RELATED],
    'ONE_GAME_SUSPENSION': [InjuryType.SUSPENSION],
    'ONE_GAME_SUSPENSION_SERVED': [InjuryType.SUSPENSION_SERVED],
    'OTHER_STINGER': [InjuryType.STINGER],
    'QUAD': [InjuryType.QUADRICEPS],
    'QUADRICEP': [InjuryType.QUADRICEPS],
    'QUARICEPS': [InjuryType.QUADRICEPS],
    'RB': [InjuryType.RIBS],
    'RIB': [InjuryType.RIBS],
    'RIBCAGE': [InjuryType.RIBS],
    'RIB_CAGE': [InjuryType.RIBS],
    'RIGHTANKLE': [InjuryType.ANKLE],
    'RIGHTCALF': [InjuryType.CALF],
    'RIGHTELBOW': [InjuryType.ELBOW],
    'RIGHTFINGER': [InjuryType.FINGER],
    'RIGHTFOOT': [InjuryType.FOOT],
    'RIGHTGROIN': [InjuryType.GROIN],
    'RIGHTHAMSTRING': [InjuryType.HAMSTRING],
    'RIGHTHAND': [InjuryType.HAND],
    'RIGHTHIP': [InjuryType.HIP],
    'RIGHTKNEE': [InjuryType.KNEE],
    'RIGHTQUADRICEP': [InjuryType.QUADRICEPS],
    'RIGHTSHIN': [InjuryType.SHIN],
    'RIGHTSHOULDER': [InjuryType.SHOULDER],
    'RIGHTTHIGH': [InjuryType.THIGH],
    'RIGHTTHUMB': [InjuryType.THUMB],
    'RIGHTUPPERARM': [InjuryType.UPPER_ARM],
    'RIGHTWRIST': [InjuryType.WRIST],
    'RIGHT_ANKLE': [InjuryType.ANKLE],
    'RIGHT_ARM': [InjuryType.ARM],
    'RIGHT_BICEPS': [InjuryType.BICEPS],
    'RIGHT_CALF': [InjuryType.CALF],
    'RIGHT_ELBOW': [InjuryType.ELBOW],
    'RIGHT_EYE': [InjuryType.EYE],
    'RIGHT_FINGER': [InjuryType.FINGER],
    'RIGHT_FOOT': [InjuryType.FOOT],
    'RIGHT_FOREARM': [InjuryType.FOREARM],
    'RIGHT_GROIN': [InjuryType.GROIN],
    'RIGHT_HAMSTRING': [InjuryType.HAMSTRING],
    'RIGHT_HAND': [InjuryType.HAND],
    'RIGHT_HIP': [InjuryType.HIP],
    'RIGHT_KNEE': [InjuryType.KNEE],
    'RIGHT_LEG': [InjuryType.LEG],
    'RIGHT_QUADRICEP': [InjuryType.QUADRICEPS],
    'RIGHT_QUADRICEPS': [InjuryType.QUADRICEPS],
    'RIGHT_SHIN': [InjuryType.SHIN],
    'RIGHT_SHOULDER': [InjuryType.SHOULDER],
    'RIGHT_THIGH': [InjuryType.THIGH],
    'RIGHT_THUMB': [InjuryType.THUMB],
    'RIGHT_TOE': [InjuryType.TOE],
    'RIGHT_UPPER_ARM': [InjuryType.UPPER_ARM],
    'RIGHT_WRIST': [InjuryType.WRIST],
    'SEVEN_GAME_SUSPENSION_SERVED': [InjuryType.SUSPENSION_SERVED],
    'SHORTNESSOFBREATH': [InjuryType.SHORTNESS_OF_BREATH],
    'SHOULDERS': [InjuryType.SHOULDER],
    'SHOULDER_BACK': [InjuryType.SHOULDER, InjuryType.BACK],
    'SHOULDER_FOOT': [InjuryType.SHOULDER, InjuryType.FOOT],
    'SHOULDET': [InjuryType.SHOULDER],
    'SIX_GAME_SUSPENSION_SERVED': [InjuryType.SUSPENSION_SERVED],
    'SPRAINED_LEFT_FOOT': [InjuryType.FOOT],
    'SPRAINED_MCL': [InjuryType.MCL],
    'SPRAINED_RIGHT_FOOT': [InjuryType.FOOT],
    'STERNOCLAVICULAR': [InjuryType.STERNUM, InjuryType.CLAVICLE],
    'TEETH': [InjuryType.DENTAL],
    'TEN_GAME_SUSPENSION_SERVED': [InjuryType.SUSPENSION_SERVED],
    'THREE_GAME_SUSPENSION_SERVED': [InjuryType.SUSPENSION_SERVED],
    'TOES': [InjuryType.TOE],
    'TOOTH': [InjuryType.DENTAL],
    'TORN_LEFT_ACL': [InjuryType.TORN_ACL],
    'TORN_PECTORAL_MUSCLE': [InjuryType.PECTORAL],
    'TORN_RIGHT_ACL': [InjuryType.TORN_ACL],
    'TRICEP': [InjuryType.TRICEPS],
    'TWO_GAME_SUSPENSION_SERVED': [InjuryType.SUSPENSION_SERVED],
    'VIRUS': [InjuryType.ILLNESS],
}
