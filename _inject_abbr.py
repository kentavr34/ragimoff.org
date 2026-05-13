#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wrap authoritative-source abbreviations in <abbr title="..."> tooltips.
Body only — skips text inside <h1>-<h6>, <title>, <abbr>, <a>, attributes, comments.
Idempotent: already-wrapped occurrences are left alone."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
TARGETS = list((ROOT / "klinik-psixiatriya").glob("*.html"))

# Longer keys must come first so they win over shorter prefixes.
ABBR = [
    ("NICE CG178", "National Institute for Health and Care Excellence — Clinical Guideline 178 (Böyük Britaniya, 2014/2019). Psychosis and schizophrenia in adults: prevention and management."),
    ("NICE CG192", "NICE Clinical Guideline 192 (2014/2018). Antenatal and postnatal mental health."),
    ("NICE CG185", "NICE Clinical Guideline 185 (2014/2020). Bipolar disorder: assessment and management."),
    ("NICE CG159", "NICE Clinical Guideline 159 (2013). Social anxiety disorder: recognition, assessment and treatment."),
    ("NICE CG113", "NICE Clinical Guideline 113 (2011/2020). Generalised anxiety disorder and panic disorder in adults: management."),
    ("NICE CG111", "NICE Clinical Guideline 111 (2010). Nocturnal enuresis in children and young people under 19."),
    ("NICE CG115", "NICE Clinical Guideline 115 (2011). Alcohol-use disorders: diagnosis, assessment and management."),
    ("NICE CG78", "NICE Clinical Guideline 78 (2009). Borderline personality disorder: recognition and management."),
    ("NICE CG31", "NICE Clinical Guideline 31 (2005). Obsessive-compulsive disorder and body dysmorphic disorder."),
    ("NICE CG170", "NICE Clinical Guideline 170 (2013). Autism spectrum disorder in under 19s: support and management."),
    ("NICE NG222", "NICE Guideline 222 (2022). Depression in adults: treatment and management."),
    ("NICE NG185", "NICE Guideline 185 (2020). Acute coronary syndromes."),
    ("NICE NG97", "NICE Guideline 97 (2018). Dementia: assessment, management and support for people living with dementia and their carers."),
    ("NICE NG87", "NICE Guideline 87 (2018). Attention deficit hyperactivity disorder: diagnosis and management."),
    ("NICE NG70", "NICE Guideline 70 (2017). Children's attachment / Antisocial behaviour and conduct disorders."),
    ("NICE NG69", "NICE Guideline 69 (2017). Eating disorders: recognition and treatment."),
    ("NICE TA59", "NICE Technology Appraisal 59 (2003). Guidance on the use of electroconvulsive therapy."),
    ("NICE", "National Institute for Health and Care Excellence — Böyük Britaniya Səhiyyə Sistemi (NHS) üçün klinik göstərişlər hazırlayan dövlət orqanı."),
    ("DSM-5-TR", "Diagnostic and Statistical Manual of Mental Disorders, 5th edition, Text Revision — American Psychiatric Association, 2022."),
    ("DSM-5", "Diagnostic and Statistical Manual of Mental Disorders, 5th edition — APA, 2013."),
    ("DSM-IV", "Diagnostic and Statistical Manual of Mental Disorders, 4th edition — APA, 1994."),
    ("DSM-III", "Diagnostic and Statistical Manual of Mental Disorders, 3rd edition — APA, 1980."),
    ("XBT-11", "Xəstəliklərin Beynəlxalq Təsnifatı, 11-ci redaksiya — Ümumdünya Səhiyyə Təşkilatı (WHO), 2019, qüvvəyə minmə 2022."),
    ("XBT-10", "Xəstəliklərin Beynəlxalq Təsnifatı, 10-cu redaksiya — WHO, 1990."),
    ("ICD-11", "International Classification of Diseases, 11th revision — WHO."),
    ("ICD-10", "International Classification of Diseases, 10th revision — WHO."),
    ("WFSBP", "World Federation of Societies of Biological Psychiatry — beynəlxalq peşəkar birlik; bioloji müalicə üzrə təlimatlar."),
    ("AACAP", "American Academy of Child and Adolescent Psychiatry — ABŞ uşaq və yeniyetmə psixiatriyası birliyi; Practice Parameters."),
    ("AASM", "American Academy of Sleep Medicine — ABŞ yuxu tibbi birliyi; Clinical Practice Guidelines."),
    ("ISSTD", "International Society for the Study of Trauma and Dissociation — travma və dissosiasiya üzrə beynəlxalq birlik."),
    ("ISSWSH", "International Society for the Study of Women's Sexual Health — qadın cinsi sağlamlığı üzrə beynəlxalq birlik."),
    ("ISSM", "International Society for Sexual Medicine — cinsi tibb üzrə beynəlxalq birlik."),
    ("ICCS", "International Children's Continence Society — uşaq uroloji və davamiyyət üzrə beynəlxalq birlik."),
    ("WPATH", "World Professional Association for Transgender Health — transgender sağlamlığı üzrə beynəlxalq birlik."),
    ("CANMAT", "Canadian Network for Mood and Anxiety Treatments — Kanada əhval və narahatlıq müalicəsi şəbəkəsi."),
    ("EACD", "European Academy of Childhood Disability — Avropa uşaq əlilliyi akademiyası."),
    ("SAMHSA", "Substance Abuse and Mental Health Services Administration — ABŞ maddə istifadəsi və psixi sağlamlıq xidmətləri idarəsi."),
    ("AAIDD", "American Association on Intellectual and Developmental Disabilities — ABŞ intellektual və inkişaf əlilliyi birliyi."),
    ("AAP", "American Academy of Pediatrics — ABŞ pediatrlar akademiyası; Clinical Reports."),
    ("AAN", "American Academy of Neurology — ABŞ nevrologiya akademiyası."),
    ("AUA", "American Urological Association — ABŞ uroloqlar birliyi."),
    ("ACOG", "American College of Obstetricians and Gynecologists — ABŞ ginekoloqlar və mama-ginekoloqlar kolleci."),
    ("ACMG", "American College of Medical Genetics — ABŞ tibbi genetika kolleci."),
    ("APA", "American Psychiatric Association — ABŞ psixiatrlar birliyi; DSM-5-TR və Practice Guidelines."),
    ("ASHA", "American Speech-Language-Hearing Association — ABŞ nitq, dil və eşitmə birliyi."),
    ("IDA", "International Dyslexia Association — beynəlxalq disleksiya birliyi."),
    ("EMA", "European Medicines Agency — Avropa dərman tənzimləyici agentliyi."),
    ("FDA", "Food and Drug Administration — ABŞ dərman və qida tənzimləyici idarəsi."),
    ("WHO", "World Health Organization — Ümumdünya Səhiyyə Təşkilatı."),
    ("ÜST", "Ümumdünya Səhiyyə Təşkilatı (WHO)."),
    ("EAU", "European Association of Urology — Avropa urologiya birliyi."),
    ("BAP", "British Association for Psychopharmacology — Britaniya psixofarmakologiya birliyi."),
    ("APA Publishing", "American Psychiatric Association Publishing — APA-nın elmi nəşriyyatı."),
    ("VA/DoD", "U.S. Department of Veterans Affairs / Department of Defense — ABŞ Veteranlar İşləri və Müdafiə Nazirliklərinin birgə klinik göstərişləri."),
    ("Cochrane", "Cochrane Collaboration — sübuta əsaslanan tibb sistemli icmal şəbəkəsi; Cochrane Database of Systematic Reviews."),
    ("RAS", "Autizm Spektri Pozuntusu (Rus dilindəki РАС-dan kalka — Расстройство Аутистического Спектра)."),
    ("ASP", "Autizm Spektri Pozuntusu."),
    ("DDHP", "Diqqət Defisiti və Hiperaktivlik Pozuntusu (ADHD)."),
    ("KDTp", "Psixoz üçün Koqnitiv-Davranış Terapiyası (Cognitive Behavioural Therapy for psychosis)."),
    ("KDT", "Koqnitiv-Davranış Terapiyası (Cognitive Behavioural Therapy, CBT)."),
    ("CBT-I", "Cognitive Behavioural Therapy for Insomnia — insomniya üçün koqnitiv-davranış terapiyası."),
    ("CBT-E", "Enhanced Cognitive Behavioural Therapy — yemə pozuntuları üçün təkmilləşdirilmiş KDT (Fairburn)."),
    ("DBT", "Dialectical Behaviour Therapy — Dialektik Davranış Terapiyası (Linehan)."),
    ("ACT", "Acceptance and Commitment Therapy — Qəbul və Bağlılıq Terapiyası."),
    ("EMDR", "Eye Movement Desensitization and Reprocessing — göz hərəkəti ilə desensibilizasiya və yenidən emal (travma müalicəsi)."),
    ("PE", "Prolonged Exposure therapy — uzun-müddətli ekspozisiya terapiyası (PTSD üçün)."),
    ("CPT", "Cognitive Processing Therapy — koqnitiv emal terapiyası (PTSD üçün)."),
    ("ERP", "Exposure and Response Prevention — ekspozisiya və reaksiyanın qarşısının alınması (OKP üçün)."),
    ("FBT", "Family-Based Treatment / Maudsley Model — ailə əsaslı müalicə (yemə pozuntuları üçün)."),
    ("IPT", "İnterpersonal Terapiya."),
    ("İPT", "İnterpersonal Terapiya."),
    ("MBT", "Mentalization-Based Treatment — mentalizasiyaya əsaslanan terapiya (Bateman & Fonagy)."),
    ("TFP", "Transference-Focused Psychotherapy — transferensiya yönəlmiş psixoterapiya."),
    ("STEPPS", "Systems Training for Emotional Predictability and Problem Solving."),
    ("PCIT", "Parent-Child Interaction Therapy — valideyn-uşaq qarşılıqlı təsir terapiyası."),
    ("MST", "Multisystemic Therapy — multisistemli terapiya."),
    ("FFT", "Functional Family Therapy — funksional ailə terapiyası."),
    ("IPS", "Individual Placement and Support — fərdi yerləşdirmə və dəstək (məşğulluq modeli)."),
    ("EIP", "Early Intervention in Psychosis — psixoz üçün erkən müdaxilə xidmətləri."),
    ("ACT komandası", "Assertive Community Treatment — icmada israrlı müalicə komandası."),
    ("LAI", "Long-Acting Injectable — uzun-müddətli inyeksion antipsixotik."),
    ("PANSS", "Positive and Negative Syndrome Scale — pozitiv və neqativ sindrom şkalası (Kay 1987)."),
    ("BPRS", "Brief Psychiatric Rating Scale — qısa psixiatrik qiymətləndirmə şkalası (Overall & Gorham 1962)."),
    ("SCID-5", "Structured Clinical Interview for DSM-5 — DSM-5 üçün strukturlaşdırılmış klinik müsahibə."),
    ("MINI", "Mini-International Neuropsychiatric Interview — qısa beynəlxalq neyropsixiatrik müsahibə."),
    ("C-SSRS", "Columbia Suicide Severity Rating Scale — Kolumbiya suisid şiddət qiymətləndirmə şkalası."),
    ("PHQ-9", "Patient Health Questionnaire-9 — pasiyent sağlamlığı sorğusu, 9 sual (depressiya skrining)."),
    ("GAD-7", "Generalized Anxiety Disorder-7 — ümumiləşmiş narahatlıq pozuntusu, 7 sual."),
    ("EPDS", "Edinburgh Postnatal Depression Scale — Edinburq postnatal depressiya şkalası."),
    ("ISI", "Insomnia Severity Index — insomniya şiddət indeksi."),
    ("EPS", "Ekstrapiramidal simptomlar — antipsixotik tərəfindən qabaq-dəyişən sistem yan təsirləri."),
    ("NMS", "Neuroleptic Malignant Syndrome — antipsixotik malign sindrom (təcili tibbi vəziyyət)."),
    ("EKT", "Elektrokonvulsiv Terapiya."),
    ("AR SN", "Azərbaycan Respublikası Səhiyyə Nazirliyi."),
    ("AR Səhiyyə Nazirliyi", "Azərbaycan Respublikası Səhiyyə Nazirliyi — milli klinik protokolların hazırlayıcı orqanı."),
    ("mhGAP", "Mental Health Gap Action Programme — WHO-nun aşağı gəlirli ölkələr üçün psixi sağlamlıq müdaxilə bələdçisi."),
    ("CDC", "Centers for Disease Control and Prevention — ABŞ Xəstəliklərə Nəzarət Mərkəzi."),
    ("RKİ", "Randomizə edilmiş Klinik İmtahan (Randomized Controlled Trial, RCT)."),
    ("RCT", "Randomized Controlled Trial — randomizə edilmiş klinik imtahan."),
    ("OAT", "Opioid Agonist Therapy — opioid asılılığında aqonist əvəzedici müalicə (metadon, buprenorfin)."),
    ("UROD", "Ultra-Rapid Opioid Detoxification — ultra-sürətli opioid detoksifikasiyası (göstərişlərdə tövsiyə edilmir)."),
    ("PSP", "Personal and Social Performance Scale — fərdi və sosial performans şkalası."),
    ("GAF", "Global Assessment of Functioning — funksional səviyyənin ümumi qiymətləndirmə şkalası."),
    ("PSQI", "Pittsburgh Sleep Quality Index — Pittsburq yuxu keyfiyyət indeksi."),
    ("M-CHAT-R/F", "Modified Checklist for Autism in Toddlers, Revised, with Follow-Up — körpələrdə autizm skrining vasitəsi."),
    ("MMR", "Measles-Mumps-Rubella vaccine — qızılca, parotit, məxmərək peyvəndi."),
    ("MMS", "Miracle Mineral Solution — klor dioksid əsaslı qondarma 'müalicə', qadağan edilmişdir."),
    ("HBOT", "Hyperbaric Oxygen Therapy — hiperbarik oksigen terapiyası."),
    ("FC", "Facilitated Communication — fasiltə kommunikasiyası (ASHA tərəfindən elmi əsaslı kimi tövsiyə edilmir)."),
    ("RPM", "Rapid Prompting Method — sürətli stimullaşdırma metodu (sübut bazası yoxdur)."),
    ("TRS", "Treatment-Resistant Schizophrenia — müalicə-rezistent şizofreniya."),
    ("DUP", "Duration of Untreated Psychosis — müalicəsiz psixoz dövrü."),
    ("DSME", "Diabetes Self-Management Education — diabetdə özünüidarə təlimi."),
    ("PDE5", "Phosphodiesterase type 5 inhibitors — fosfodiesteraza tip 5 inhibitorları (sildenafil, tadalafil, vardenafil, avanafil)."),
    ("TRT", "Testosterone Replacement Therapy — testosteron əvəzedici terapiya."),
    ("HSDD", "Hypoactive Sexual Desire Disorder — hipoaktiv cinsi istək pozuntusu."),
    ("IIEF", "International Index of Erectile Function — beynəlxalq erektil funksiya indeksi."),
    ("FSFI", "Female Sexual Function Index — qadın cinsi funksiya indeksi."),
    ("CSC", "Coordinated Specialty Care — koordinə edilmiş ixtisaslaşdırılmış qayğı (psixoz üçün)."),
    ("RAISE", "Recovery After an Initial Schizophrenia Episode — ilk şizofreniya epizodundan sonra bərpa proqramı (NIMH)."),
    ("EE", "Expressed Emotion — ailənin emosional ekspressiya səviyyəsi."),
    ("OKP", "Obsessiv-Kompulsiv Pozuntu."),
    ("PTSP", "Posttravmatik Stress Pozuntusu."),
    ("PPD", "Postpartum Depression — postnatal depressiya."),
    ("PPP", "Postpartum Psychosis — postnatal psixoz."),
    ("UTI", "Urinary Tract Infection — sidik yolları infeksiyası."),
    ("CRP", "C-Reactive Protein — iltihab markerı."),
    ("NMDA", "N-Methyl-D-Aspartate — qlutamat reseptor növü."),
    ("GABA", "Gamma-Aminobutyric Acid — beynin əsas inhibitor neyrotransmitteri."),
    ("CNV", "Copy Number Variation — gen nüsxə sayı dəyişikliyi."),
    ("GWAS", "Genome-Wide Association Study — bütün genoma üzrə assosiasiya tədqiqatı."),
    ("CGI-S", "Clinical Global Impression — Severity — klinik ümumi təəssürat şiddət şkalası."),
    ("CSF", "Cerebrospinal Fluid — beyin-onurğa beyni mayesi."),
    ("PCP", "Phencyclidine — disossiativ psixoaktiv maddə."),
    ("THC", "Tetrahydrocannabinol — kannabisin əsas psixoaktiv komponenti."),
    ("CBD", "Cannabidiol — kannabis bitkisinin qeyri-psixoaktiv komponenti."),
    ("SSRI", "Selective Serotonin Reuptake Inhibitor — selektiv serotonin geri-götürülmə inhibitoru."),
    ("SNRI", "Serotonin-Norepinephrine Reuptake Inhibitor — serotonin və noradrenalin geri-götürülmə inhibitoru."),
    ("CPK", "Creatine Phosphokinase — kreatin fosfokinaza (əzələ zədəsi markerı)."),
    ("HbA1c", "Glikolaşdırılmış hemoqlobin — son 2–3 ayın qan şəkəri orta göstəricisi."),
    ("MRT", "Maqnit Rezonans Tomoqrafiya."),
    ("EEQ", "Elektroensefaloqrafiya."),
    ("EKG", "Elektrokardioqrafiya."),
    ("TSH", "Thyroid-Stimulating Hormone — tireotropin."),
    ("ADH", "Antidiuretik Hormon — vasopressin."),
    ("AD", "Antidepresant."),
]

# Don't wrap if the key is purely alphabetic and very short and could be a common word.
# We rely on uppercase / hyphenated patterns which are unlikely to collide.

CSS_RULE = """
  abbr[title]{ text-decoration: underline dotted; text-underline-offset: 2px; cursor: help; }
"""

def build_replacer():
    """Single-pass replacer: longest key wins; output is not rescanned
    (re.sub processes left-to-right and doesn't reenter substitutions),
    so we cannot accidentally wrap a token that appears in another's title."""
    keys_sorted = sorted(ABBR, key=lambda x: -len(x[0]))
    titles = {k: t.replace('"', '&quot;') for k, t in ABBR}
    alt = "|".join(re.escape(k) for k, _ in keys_sorted)
    big = re.compile(
        r'(?<![A-Za-z0-9_-])(' + alt + r')(?![A-Za-z0-9_-])'
    )

    def _sub(m):
        k = m.group(1)
        return f'<abbr title="{titles[k]}">{k}</abbr>'

    def repl(text):
        return big.sub(_sub, text)
    return repl


# Regex matchers
HEADING_RE = re.compile(r'(<h[1-6]\b[^>]*>.*?</h[1-6]>)', re.DOTALL | re.IGNORECASE)
TAG_BLOCK_RE = re.compile(r'(<title\b.*?</title>|<script\b.*?</script>|<style\b.*?</style>|<a\b[^>]*>.*?</a>|<!--.*?-->)', re.DOTALL | re.IGNORECASE)
ATTR_RE = re.compile(r'(\s[a-zA-Z-]+="[^"]*"|\s[a-zA-Z-]+=\'[^\']*\')')


def inject_css_link(html: str) -> str:
    """Add abbr CSS once into <head>."""
    if "/* duzelis-abbr-style */" in html:
        return html
    snippet = f'<style>/* duzelis-abbr-style */{CSS_RULE}</style>'
    return html.replace("</head>", f"  {snippet}\n</head>", 1)


def process_html(html: str) -> str:
    """Wrap abbreviations in body text only."""
    repl = build_replacer()
    # Split out all "no-touch" blocks (headings + script/style/title/a/comments).
    # We keep a flat token list: even tokens are "body" (process), odd tokens
    # are "preserved" (skip).
    NO_TOUCH = re.compile(
        r'(<h[1-6]\b[^>]*>.*?</h[1-6]>'
        r'|<title\b.*?</title>'
        r'|<script\b.*?</script>'
        r'|<style\b.*?</style>'
        r'|<a\b[^>]*>.*?</a>'
        r'|<!--.*?-->)',
        re.DOTALL | re.IGNORECASE,
    )
    parts = NO_TOUCH.split(html)
    for i in range(0, len(parts), 2):
        body = parts[i]
        # Inside body, also avoid touching tag-attribute strings:
        # do substitution only on text content, not within tags.
        # Split by < ... >
        tag_parts = re.split(r'(<[^>]+>)', body)
        for j in range(0, len(tag_parts), 2):  # even = text outside tags
            tag_parts[j] = repl(tag_parts[j])
        parts[i] = "".join(tag_parts)
    return "".join(parts)


def main():
    total = 0
    for p in TARGETS:
        text = p.read_text(encoding="utf-8")
        new = process_html(text)
        new = inject_css_link(new)
        if new != text:
            p.write_text(new, encoding="utf-8")
            # Count abbr wraps added
            added = new.count('<abbr title="') - text.count('<abbr title="')
            print(f"{added:4d}  {p.name}")
            total += added
    print(f"\nTotal abbr wrappings added: {total}")


if __name__ == "__main__":
    main()
