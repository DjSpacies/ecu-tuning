"""Topic and platform taxonomy for the corpus index. Regexes are matched case-insensitively; use (?-i:...) where
case matters (CAN, ETC are ordinary English words in lower case). Words that also occur in plain English or in
another field need a narrow pattern: the gap report is only as good as this list.

EXPECT says which source classes each topic must be backed by; the gap report checks exactly those:
  P engineering references  T control/statistics theory  L Link G4+ help  V other vendor docs  I instruction (practitioner training, practitioner training)
"""

TOPICS = {
    # L0 / L1 fundamentals
    "airflow-ve":        [r"volumetric efficiency", r"(?<!['\u2019])\bve\b", r"\bairflow\b", r"air ?mass", r"air density", r"cylinder filling", r"\bbreathing\b"],
    "combustion-afr":    [r"\blambda\b", r"\bafr\b", r"air ?fuel ratio", r"\bstoich", r"\brich(?:er)?\b", r"\blean(?:er)?\b", r"\bcombustion\b"],
    "combustion-pressure": [r"cylinder pressure", r"heat release", r"mass fraction burn", r"burn rate", r"\bpeak pressure\b", r"\bimep\b", r"\bbmep\b"],
    "ignition-mbt":      [r"ignition timing", r"\bmbt\b", r"spark advance", r"ignition advance", r"timing advance", r"\bretard"],
    "knock":             [r"\bknock", r"detonation", r"pre-?ignition", r"\bend[- ]gas\b", r"\bautoignition\b"],
    "fuels":             [r"ethanol", r"\be85\b", r"methanol", r"octane", r"fuel properties", r"race fuel", r"latent heat", r"\bron\b", r"reid vapou?r"],
    "flex-fuel":         [r"flex ?fuel", r"ethanol content", r"ethanol sensor", r"fuel composition", r"multi ?fuel"],
    "thermo-charge-temp":[r"charge temp", r"intake air temp", r"\biat\b", r"charge cooling", r"heat soak", r"intercool"],
    # Fuel system
    "injectors":         [r"injector", r"dead ?time", r"short pulse", r"pulse ?width", r"duty cycle"],
    "fuel-system":       [r"fuel pump", r"fuel pressure", r"pressure regulator", r"fuel system", r"surge tank", r"return(?:less)? (?:fuel|line|system)"],
    "injection-timing":  [r"injection timing", r"end of injection", r"open[- ]valve injection", r"closed[- ]valve injection", r"injection phasing", r"\beoi\b", r"staged injection", r"secondary injector"],
    "direct-injection":  [r"direct injection", r"\bgdi\b", r"\bdi injector", r"high pressure pump", r"stratified"],
    # Load / fuel models / tables
    "fuel-model-load":   [r"fuel model", r"modelled", r"speed[- ]?density", r"mean[- ]value", r"manifold filling", r"air[- ]charge", r"cylinder charge", r"air[- ]mass meter", r"load (?:signal|detection)", r"alpha-?n", r"\bmap\b sensor", r"\bmaf\b", r"load axis", r"table resolution", r"breakpoint"],
    "compensations":     [r"compensation", r"correction table", r"fuel correction", r"ignition correction", r"temp(?:erature)? correction", r"\bbaro\b", r"coolant temp", r"trim table"],
    # Tuning procedures
    "steady-state-fuel": [r"fuel tuning", r"steady state", r"ve table", r"fuel table"],
    "transients":        [r"acceleration enrichment", r"accel(?:eration)? enrich", r"\btransient", r"wall wetting", r"tip-?in", r"fuel film"],
    "closed-loop":       [r"closed loop (?:fuel|lambda|control)", r"short term trim", r"long term trim", r"\bstft\b", r"\bltft\b", r"o2 feedback", r"\bcll\b"],
    "start-warmup":      [r"cold start", r"cranking", r"warm-?up", r"post start", r"after ?start"],
    "idle":              [r"\bidle\b", r"\bidling\b"],
    "cylinder-trim":     [r"individual cylinder", r"cylinder trim", r"per cylinder", r"\begt\b"],
    # Air control
    "boost-control":     [r"boost control", r"wastegate", r"waste gate", r"boost target", r"boost pid", r"boost feed ?forward", r"closed loop boost", r"open loop boost"],
    "turbo-fi":          [r"turbo", r"supercharg", r"forced induction", r"compressor map", r"pressure ratio"],
    "cam-vvt":           [r"\bvvt\b", r"cam control", r"variable cam", r"cam timing", r"cam angle", r"valve timing", r"valve overlap"],
    "etc-throttle":      [r"e-?throttle", r"drive by wire", r"electronic throttle", r"(?-i:\bETC\b)", r"\bdbw\b"],
    # Motorsport functions / protection
    "launch-antilag-tc": [r"launch control", r"anti-?lag", r"traction control", r"flat shift", r"rolling launch", r"paddle shift", r"gear cut", r"shift control"],
    "engine-protection": [r"engine protection", r"limiter", r"rev limit", r"fuel cut", r"failsafe"],
    "overrun":           [r"overrun", r"over-?run", r"decel(?:eration)? fuel cut", r"\bdfco\b"],
    # Setup / electronics
    "triggers-sync":     [r"trigger (?:wheel|offset|pattern|mode|setup|error|calibration|scope|decoder|[12]\b)", r"crank (?:angle )?sensor", r"cam sensor", r"missing tooth", r"\bsync(?:hroni[sz]ation)?\b"],
    "sensors-io":        [r"sensor calibration", r"analog input", r"digital input", r"auxiliary output", r"\bpwm\b", r"\bwiring\b", r"thermistor"],
    "base-setup":        [r"base timing", r"timing light", r"initial setup", r"base map", r"first start", r"base fuel pressure"],
    "can-bus":           [r"(?-i:\bCAN\b)", r"\bcan ?bus\b", r"\bcan (?:id|message|frame|stream|network|protocol|dash)\b", r"\bdash ?(?:board|display|logger)\b", r"\bpdm\b"],
    # Process / environment
    "data-logging":      [r"data ?log", r"\blogging\b", r"log file", r"log analysis", r"\bi2\b", r"math channel"],
    "dyno":              [r"\bdyno", r"load cell", r"ramp rate", r"inertia dyno"],
    "dyno-correction":   [r"correction factor", r"\bj1349\b", r"power correction", r"atmospheric correction", r"(?:standard|reference) (?:atmospheric|ambient) conditions", r"reference conditions", r"\bsae (?:power|corrected)\b", r"\bstp\b correct", r"corrected (?:power|torque)"],
    "road-tuning":       [r"road tun", r"street tun", r"without a dyno", r"on the road"],
    "tuning-process":    [r"tuning process", r"10[- ]step", r"tuning order", r"tuning procedure", r"\bstep \d+:"],
    "reflash":           [r"reflash", r"\becu ?tek\b", r"hp ?tuners", r"winols", r"\bpcm\b", r"oem ecu"],
    "rotary":            [r"rotary (?:engine|tuning|ignition)", r"tuning rotary", r"wankel", r"\b13b\b", r"\b20b\b", r"renesis", r"(?:leading|trailing) (?:spark|coil|plug)"],
    "nitrous-wmi":       [r"nitrous", r"water ?meth", r"water injection"],
    "wideband-sensors":  [r"wideband", r"wide[- ]band", r"oxygen sensor", r"lambda sensor", r"\bo2 sensor", r"transport delay", r"sensor (?:lag|delay)"],
    "ignition-hardware": [r"\bdwell\b", r"ignition coil", r"spark plug", r"coil charge", r"ignition driver?s?\b"],
    "exhaust-backpressure": [r"exhaust back ?pressure", r"exhaust manifold pressure", r"\bemap\b", r"back ?pressure"],
    "catalyst-emissions":[r"catalytic converter", r"\bcatalyst\b", r"\bnox\b", r"emissions?\b"],
    # Theory the skill's calculators and data checks rest on
    "control-theory":    [r"\bpid\b", r"feedback control", r"feed ?forward", r"gain schedul", r"anti-?windup", r"ziegler", r"transfer function"],
    "data-quality-stats":[r"standard deviation", r"confidence interval", r"\boutliers?\b", r"least squares", r"measurement uncertainty", r"repeatability"],
}

EXPECT = {
    "airflow-ve": "PIL", "combustion-afr": "PI", "combustion-pressure": "P", "ignition-mbt": "PIL", "knock": "PIL",
    "fuels": "PI", "flex-fuel": "PIL", "thermo-charge-temp": "PIL", "injectors": "PIL", "fuel-system": "PI",
    "injection-timing": "PIL", "direct-injection": "PI", "fuel-model-load": "PIL", "compensations": "IL",
    "steady-state-fuel": "IL", "transients": "PIL", "closed-loop": "IL", "start-warmup": "IL", "idle": "IL",
    "cylinder-trim": "IL", "boost-control": "IL", "turbo-fi": "PI", "cam-vvt": "PIL", "etc-throttle": "IL",
    "launch-antilag-tc": "IL", "engine-protection": "IL", "overrun": "IL", "triggers-sync": "IL", "sensors-io": "IL",
    "base-setup": "IL", "can-bus": "IL", "data-logging": "IL", "dyno": "I", "dyno-correction": "PI", "road-tuning": "I",
    "tuning-process": "I", "reflash": "IV", "rotary": "I", "nitrous-wmi": "I", "control-theory": "T",
    "data-quality-stats": "T", "wideband-sensors": "PIL", "ignition-hardware": "PIL", "exhaust-backpressure": "PI",
    "catalyst-emissions": "P",
}

PLATFORMS = {
    "link-g4plus": [r"link g4\+", r"link g4 ?plus", r"g4\+", r"\bvipec\b", r"\blink g4\b"],
    "link-g4x":    [r"\bg4x\b"],
    "link-g5":     [r"\bg5\b"],
    "motec-m1":    [r"motec m1", r"\bm1 (?:tune|build|ecu|package|series)\b"],
    "motec-m150":  [r"\bm150\b", r"\bm1\d\d\b"],
    "motec-other": [r"\bmotec\b"],
    "haltech":     [r"haltech", r"elite 2500", r"platinum pro"],
    "aem":         [r"\baem\b", r"infinity ?tuner", r"\binfinity (?:ecu|series)\b"],
    "fueltech":    [r"fuel ?tech", r"ft600"],
    "emtron":      [r"emtron"],
    "megasquirt":  [r"megasquirt"],
    "speeduino":   [r"speeduino"],
    "ecumaster":   [r"ecu ?masters?"],
    "maxxecu":     [r"maxx ?ecu"],
    "holley":      [r"holley"],
    "adaptronic":  [r"adaptronic"],
    "hondata":     [r"hondata", r"k-?pro", r"flashpro", r"s300"],
    "reflash-tools": [r"hp ?tuners", r"ecu ?tek", r"winols", r"cobb", r"ecu ?flash"],
}

# Narrow topics a short standard can settle: the engineering-reference passages needed (default --min-passages).
MIN_PASSAGES = {"dyno-correction": 3}

# A passage of a long document dense in these is about diesel engines, which are out of scope.
DIESEL = [r"\bdiesels?\b", r"compression[- ]ignition", r"\bcommon[- ]rail\b", r"\bunit injector"]

# Vendor documentation belongs to its platform whatever words it uses.
VENDOR_PLATFORM = {
    "link/pclink-g4plus": ["link-g4plus"], "link/pclink-g4x": ["link-g4x", "link-g5"], "haltech": ["haltech"],
    "motec": ["motec-other"], "aem": ["aem"], "fueltech": ["fueltech"], "msextra": ["megasquirt"], "speeduino": ["speeduino"],
    "ecumaster": ["ecumaster"], "maxxecu": ["maxxecu"], "holley": ["holley"], "hondata": ["hondata"],
    "cobb": ["reflash-tools"], "ecutek": ["reflash-tools"], "hptuners": ["reflash-tools"], "winols": ["reflash-tools"],
}
