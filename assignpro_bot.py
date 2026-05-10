"""
AssignPro Solution — Telegram Bot (Upgraded)
Full client acquisition bot with samples, guides, quotes & lead capture
Requirements: python-telegram-bot==21.9
"""

import logging
import os
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── CONFIG ────────────────────────────────────────────────────────────────────
BOT_TOKEN    = os.getenv("BOT_TOKEN", "")
ADMIN_ID     = 800268202
WHATSAPP_NUM = "918946906702"
WHATSAPP_URL = f"https://wa.me/{WHATSAPP_NUM}"
WEBSITE_UK   = "https://uk.assignprosolution.com"
WEBSITE_AU   = "https://au.assignprosolution.com"
WEBSITE_UAE  = "https://ae.assignprosolution.com"
WEBSITE_CA   = "https://ca.assignprosolution.com"

# ─── STUDY PURPOSE WARNING ─────────────────────────────────────────────────────
STUDY_WARNING = (
    "\n\n"
    "⚠️ *IMPORTANT NOTICE — FOR STUDY PURPOSES ONLY*\n"
    "All samples and materials provided are strictly for reference and learning.\n"
    "❌ Do NOT copy, submit, or present this work as your own.\n"
    "✅ Use it to understand structure, style, and formatting only.\n"
    "We are not responsible for any misuse of these materials."
)

# Conversation states
(QUOTE_SUBJECT, QUOTE_DEADLINE, QUOTE_WORDS,
 QUOTE_DETAILS, QUOTE_CONTACT) = range(5)

# ─── SAMPLE FILE IDs ───────────────────────────────────────────────────────────
# Replace YOUR_FILE_ID_X with real Telegram file_ids after uploading
SAMPLES = {
    # ── ESSAYS ──
    "essay_business":     {"name": "Essay — Business Management (2:1 Grade, 2000 words)",          "file_id": "BQACAgUAAxkBAAM1af92_O2Fr3NPHkcTNM2u9uA_V4UAAkAfAALm3fhXdi_upJYeR3o7BA"},
    "essay_marketing":    {"name": "Essay — International Business (2:1 Grade, 2000 words)",        "file_id": "BQACAgUAAxkBAANragABJOPHnh-vVBWb3z1PhP5EfdjuAAKwGgACdgkAAVQ0Z09pKw9KNDsE"},
    "essay_psychology":   {"name": "Essay — Psychology & Mental Health (2:1 Grade, 2500 words)",    "file_id": "BQACAgUAAxkBAANhagABJEsnLjweXR7wIW0EvPUltF0tAAKsGgACdgkAAVRoFcel0lJW2TsE"},
    "essay_leadership":   {"name": "Essay — Leadership & Motivation (First Class, 2500 words)",     "file_id": "BQACAgUAAxkBAANWaf9_tQLiKwKQJj3ANTw7fjJnh1IAAlAfAALm3fhX8LCEX8yBZYo7BA"},
    "essay_child_dev": {"name": "Essay — Child Development & Attachment Theory (2:1 Grade, 2000 words)", "file_id": "BQACAgUAAxkBAANaagABJBZ2enbFLH74tozrqaDUXa3UAAKpGgACdgkAAVT8mRJJGR4yLzsE"},
    "essay_economics": {"name": "Essay — Economics & Monetary Policy (2:1 Grade, 2500 words)", "file_id": "BQACAgUAAxkBAANeagABJDlPKtBpzRZtx0TfaMcbzJhwAAKrGgACdgkAAVQG2KyXkl0GizsE"},
    "essay_education": {"name": "Essay — Education Studies & Inclusive Learning (First Class, 2000 words)", "file_id": "BQACAgUAAxkBAANkagABJFwjsvSD-QsJg32HeMMbepJOAAKtGgACdgkAAVTno5r1kbojyTsE"},
    "essay_env_law": {"name": "Essay — Environmental Law & Climate Litigation (First Class, 3000 words)", "file_id": "BQACAgUAAxkBAANnagABJHW0Xx7jzDgDXf5Hi3eknDeMAAKuGgACdgkAAVTh8A5kJS7uyTsE"},
    "essay_media": {"name": "Essay — Media, Communications & Misinformation (First Class, 2000 words)", "file_id": "BQACAgUAAxkBAANuagABJTU8Jgd0fsO-KbuzgZV_niUWAAKxGgACdgkAAVREnkmZdgl1wTsE"},
    "essay_social_work": {"name": "Essay — Social Work & Person-Centred Practice (First Class, 2500 words)", "file_id": "BQACAgUAAxkBAAN3agABJcGpZblmIAL0Rcee-wv7FFYyAAK0GgACdgkAAVQI1505_4XqYjsE"},
    "essay_public_health": {"name": "Essay — Public Health Policy & Inequalities (2:1 Grade, 2000 words)", "file_id": "BQACAgUAAxkBAAN6agABJeqyMmBSYi29AAFCfbFnS-yAdgACtRoAAnYJAAFU_NJSYl3Y9Lk7BA"},
    "essay_hrm": {"name": "Essay — Human Resource Management (First Class, 2500 words)", "file_id": "BQACAgUAAxkBAAN9agABJjabzA0lIbyh2rug4hRYkFh2AAK3GgACdgkAAVSzgDq9iFMSHjsE"},
    "essay_criminology": {"name": "Essay — Criminology & Strain Theory (2:1 Grade, 2000 words)", "file_id": "BQACAgUAAxkBAAOAagABJnmRh_b19lRSNUrHW89BIf6FAAK4GgACdgkAAVTLYHNlS6j6BjsE"},

    # ── DISSERTATIONS ──
    "dissertation_nurse": {"name": "Dissertation — Nursing (First Class, 10000 words)",             "file_id": "YOUR_FILE_ID_4"},
    "dissertation_mba":   {"name": "Dissertation — MBA Finance (Distinction, 12000 words)",         "file_id": "BQACAgUAAxkBAAMaaf91oCC_g8A9-Ot3NG-Nd7rYKdoAAiwfAALm3fhXKHMRL4oUhgw7BA"},
    # ── CASE STUDIES ──
    "case_study_law":     {"name": "Case Study — Law & Contract (2:1 Grade)",                       "file_id": "YOUR_FILE_ID_6"},
    "case_study_mba":     {"name": "Case Study — MBA Strategy (First Class)",                       "file_id": "BQACAgUAAxkBAAMsaf92n5bFXAbwrXk4DQEgZKCs9QcAAjkfAALm3fhXNzQcXuxLKbE7BA"},
    "case_study_redbull": {"name": "Case Study — Red Bull Marketing Strategy (First Class)",        "file_id": "BQACAgUAAxkBAANHaf9_JR-eawsuxKIMdUZyxG57fe4AAksfAALm3fhXhJIZ3QY3GRo7BA"},
    "case_study_cocacola":{"name": "Case Study — Coca-Cola Marketing Strategy (2:1 Grade)",        "file_id": "BQACAgUAAxkBAANKaf9_RenVLs9Exx0bbJjysMWo8SIAAkwfAALm3fhX28o8PiCxg5c7BA"},
    # ── REPORTS ──
    "report_engineering": {"name": "Report — Sustainable Energy & Engineering (2:1 Grade, 3000 words)", "file_id": "BQACAgUAAxkBAANEaf9-8mm3eSVyQQFx-DUaW4l3uZEAAkofAALm3fhX30DMIiQM6447BA"},
    "report_finance":     {"name": "Report — Financial Analysis (First Class, 2500 words)",         "file_id": "YOUR_FILE_ID_9"},
    "report_ml":          {"name": "Report — Machine Learning in Healthcare (2:1 Grade, 3000 words)","file_id": "BQACAgUAAxkBAANBaf9-IuDU6hkS-uDlo7-53oPXHDoAAkgfAALm3fhXXOOhoxP246M7BA"},
    # ── LITERATURE REVIEWS ──
    "literature_psych":   {"name": "Literature Review — Psychology (2:1 Grade, 3000 words)",        "file_id": "BQACAgUAAxkBAAMmaf92TqL67YI11d7c6iAUV8ke-fIAAjMfAALm3fhX87N2XUr0fPQ7BA"},
    "literature_health":  {"name": "Literature Review — Healthcare (First Class, 4000 words)",      "file_id": "BQACAgUAAxkBAAMeaf92AlKXM436p6h0MSua5nV9-bwAAi8fAALm3fhXnNRavrm8m907BA"},
    "literature_social":  {"name": "Literature Review — Social Media & Mental Health (2:1 Grade)",  "file_id": "BQACAgUAAxkBAAN3agABJcGpZblmIAL0Rcee-wv7FFYyAAK0GgACdgkAAVQI1505_4XqYjsE"},
    # ── NURSING ──
    "nursing_care":       {"name": "Nursing — Care Plan Assignment (2:1 Grade)",                    "file_id": "BQACAgUAAxkBAAMhaf92Fc9BLA-BoZ1RUYd0Ya7C0KUAAjAfAALm3fhXM1V8Wcu2daw7BA"},
    "nursing_reflection": {"name": "Nursing — Clinical Reflection (First Class)",                   "file_id": "BQACAgUAAxkBAAMyaf924zLSUoQHXDYWY2OcFyEQBwsAAj8fAALm3fhXGqlWEZ9eGx07BA"},
    "nursing_care_plan":  {"name": "Nursing — Post-Operative Care Plan Essay (First Class)",        "file_id": "BQACAgUAAxkBAANTaf9_okd2pmDjp_HtBiaaZ_D7kocAAk8fAALm3fhX05-E9az5t047BA"},
    "nursing_mental_health":  {"name": "Nursing — Mental Health Assessment & Care Planning (First Class)", "file_id": "BQACAgUAAxkBAAOZagABNZZpBdhjFjLJWFPgVhuhl82eAALdGgACdgkAAVT6UyP_-0FZPjsE"},
    "nursing_safeguarding":   {"name": "Nursing — Safeguarding Children (2:1 Grade)",                      "file_id": "PLACEHOLDER_safeguarding"},
    "nursing_medicines":      {"name": "Nursing — Medicines Management & Safe Administration (First Class)","file_id": "BQACAgUAAxkBAAOSagABNURX6w-MLireM6moVUKNfLHMAALaGgACdgkAAVT9fB5ko8DbeTsE"},
    "nursing_eol":            {"name": "Nursing — End of Life Care (2:1 Grade)",                           "file_id": "BQACAgUAAxkBAAOJagABNQTpI006pvn8ic17Pu8jQ_f7AALXGgACdgkAAVQOH-xBv5ColzsE"},
    "nursing_dementia":       {"name": "Nursing — Person-Centred Dementia Care (2:1 Grade)",               "file_id": "BQACAgUAAxkBAAOGagABNPQsIKPJsT9FhqoDn3W3C7GdAALWGgACdgkAAVRp3fyIVliveDsE"},
    "nursing_infection":      {"name": "Nursing — Infection Prevention & Control (First Class)",           "file_id": "BQACAgUAAxkBAAOPagABNTOcoTS3upXsfII4vS0WPy2dAALZGgACdgkAAVTpJU_qFl8AAew7BA"},
    "nursing_midwifery":      {"name": "Nursing — Woman-Centred Midwifery Practice (First Class)",         "file_id": "BQACAgUAAxkBAAOWagABNV0_JGIAAYzOfQtNBWqfI_XfFAAC3BoAAnYJAAFUaILfLhHVNYg7BA"},
    "nursing_diabetes":       {"name": "Nursing — Type 2 Diabetes Management (2:1 Grade)",                "file_id": "BQACAgUAAxkBAAOcagABNbTkSXH-kVtnxYVJbozhUSroAALeGgACdgkAAVRgUdrl_dOX5TsE"},
    # ── COMPUTER SCIENCE ──
    "cs_python":          {"name": "Computer Science — Python Programming Report",                  "file_id": "YOUR_FILE_ID_14"},
    "cs_ai":              {"name": "Computer Science — AI/ML Research Paper (2:1 Grade)",           "file_id": "YOUR_FILE_ID_15"},
    # ── LAW ──
    "law_essay":          {"name": "Law — Criminal Law Essay (First Class, OSCOLA)",                "file_id": "BQACAgUAAxkBAANQaf9_hhu5j2wo7zNnZV2r3QJbBfwAAk4fAALm3fhX2FvDbP22SyY7BA"},
    "law_tort":           {"name": "Law — Tort Law & Negligence Essay (2:1 Grade, OSCOLA)",        "file_id": "BQACAgUAAxkBAANNaf9_Z35aAoG6QriO8GV7O4CPz5MAAk0fAALm3fhXmej01tDfvao7BA"},
    "law_contract":    {"name": "Law — Contract Law: Offer, Acceptance & Consideration (First Class)", "file_id": "PLACEHOLDER_law_contract"},
    "law_employment":  {"name": "Law — Employment Law: Unfair Dismissal (2:1 Grade)",                  "file_id": "PLACEHOLDER_law_employment"},
    "law_human_rights":{"name": "Law — Human Rights Act 1998 (First Class)",                           "file_id": "PLACEHOLDER_law_human_rights"},
    "law_company":     {"name": "Law — Company Law: Directors Duties (2:1 Grade)",                     "file_id": "PLACEHOLDER_law_company"},
    "law_land":        {"name": "Law — Land Law: Adverse Possession (First Class)",                    "file_id": "PLACEHOLDER_law_land"},
    "law_family":      {"name": "Law — Family Law: Best Interests of the Child (2:1 Grade)",           "file_id": "PLACEHOLDER_law_family"},
}

GUIDES = {
    "harvard":       {"name": "Harvard Referencing — Complete Guide PDF",           "file_id": "YOUR_FILE_ID_G1"},
    "apa":           {"name": "APA 7th Edition — Full Referencing Guide",           "file_id": "YOUR_FILE_ID_G2"},
    "oscola":        {"name": "OSCOLA Legal Referencing — Complete Guide",           "file_id": "YOUR_FILE_ID_G3"},
    "essay_guide":   {"name": "How to Write a UK 2:1 Essay — Step by Step",         "file_id": "YOUR_FILE_ID_G4"},
    "diss_guide":    {"name": "Dissertation Success Guide — 10,000 Words",           "file_id": "YOUR_FILE_ID_G5"},
    "turnitin":      {"name": "How to Make Work Turnitin-Safe — Guide",              "file_id": "YOUR_FILE_ID_G6"},
    "nursing_guide": {"name": "Nursing Assignments Guide — NMC Standards",           "file_id": "YOUR_FILE_ID_G7"},
    "critical":      {"name": "Critical Thinking & Analysis Guide for UK Students",  "file_id": "YOUR_FILE_ID_G8"},
}

# ─── KEYBOARDS ─────────────────────────────────────────────────────────────────
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Get a Free Quote",   callback_data="quote")],
        [InlineKeyboardButton("📄 View Sample Work",   callback_data="samples"),
         InlineKeyboardButton("📚 Free Guides",        callback_data="guides")],
        [InlineKeyboardButton("💰 Pricing",            callback_data="pricing"),
         InlineKeyboardButton("⭐ Reviews",            callback_data="reviews")],
        [InlineKeyboardButton("🌍 Our Services",       callback_data="services"),
         InlineKeyboardButton("❓ FAQ",                callback_data="faq")],
        [InlineKeyboardButton("💬 Talk to a Human",    callback_data="human")],
        [InlineKeyboardButton("📱 WhatsApp Us Now",    url=WHATSAPP_URL)],
    ])

def samples_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Essays",             callback_data="samples_essays")],
        [InlineKeyboardButton("🎓 Dissertations",      callback_data="samples_dissertations")],
        [InlineKeyboardButton("📊 Case Studies",       callback_data="samples_casestudies")],
        [InlineKeyboardButton("📋 Reports",            callback_data="samples_reports")],
        [InlineKeyboardButton("📚 Literature Reviews", callback_data="samples_literature")],
        [InlineKeyboardButton("💊 Nursing",            callback_data="samples_nursing")],
        [InlineKeyboardButton("💻 Computer Science",   callback_data="samples_cs")],
        [InlineKeyboardButton("⚖️ Law",                callback_data="samples_law")],
        [InlineKeyboardButton("« Back to Menu",        callback_data="main_menu")],
    ])

def essay_samples_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Business Management",       callback_data="sample_essay_business")],
        [InlineKeyboardButton("📝 International Business",    callback_data="sample_essay_marketing")],
        [InlineKeyboardButton("📝 Psychology & Mental Health",callback_data="sample_essay_psychology")],
        [InlineKeyboardButton("📝 Leadership & Motivation",   callback_data="sample_essay_leadership")],
        [InlineKeyboardButton("📝 Human Resource Management", callback_data="sample_essay_hrm")],
        [InlineKeyboardButton("📝 Child Development",         callback_data="sample_essay_child_dev")],
        [InlineKeyboardButton("📝 Economics & Finance",       callback_data="sample_essay_economics")],
        [InlineKeyboardButton("📝 Public Health Policy",      callback_data="sample_essay_public_health")],
        [InlineKeyboardButton("📝 Social Work Practice",      callback_data="sample_essay_social_work")],
        [InlineKeyboardButton("📝 Criminology",               callback_data="sample_essay_criminology")],
        [InlineKeyboardButton("📝 Media & Communications",    callback_data="sample_essay_media")],
        [InlineKeyboardButton("📝 Environmental Law",         callback_data="sample_essay_env_law")],
        [InlineKeyboardButton("📝 Education Studies",         callback_data="sample_essay_education")],
        [InlineKeyboardButton("« Back to Samples",            callback_data="samples")],
    ])

def dissertation_samples_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎓 Nursing Dissertation",  callback_data="sample_dissertation_nurse")],
        [InlineKeyboardButton("🎓 MBA Dissertation",      callback_data="sample_dissertation_mba")],
        [InlineKeyboardButton("« Back to Samples",        callback_data="samples")],
    ])

def case_study_samples_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Law Case Study",      callback_data="sample_case_study_law")],
        [InlineKeyboardButton("📊 MBA Case Study",      callback_data="sample_case_study_mba")],
        [InlineKeyboardButton("📊 Red Bull Case Study", callback_data="sample_case_study_redbull")],
        [InlineKeyboardButton("📊 Coca-Cola Case Study",callback_data="sample_case_study_cocacola")],
        [InlineKeyboardButton("« Back to Samples",      callback_data="samples")],
    ])

def report_samples_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Engineering Report",        callback_data="sample_report_engineering")],
        [InlineKeyboardButton("📋 Finance Report",            callback_data="sample_report_finance")],
        [InlineKeyboardButton("📋 Machine Learning Report",   callback_data="sample_report_ml")],
        [InlineKeyboardButton("« Back to Samples",            callback_data="samples")],
    ])

def literature_samples_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Psychology Lit Review",       callback_data="sample_literature_psych")],
        [InlineKeyboardButton("📚 Healthcare Lit Review",       callback_data="sample_literature_health")],
        [InlineKeyboardButton("📚 Social Media & Mental Health",callback_data="sample_literature_social")],
        [InlineKeyboardButton("« Back to Samples",              callback_data="samples")],
    ])

def nursing_samples_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💊 Care Plan",                   callback_data="sample_nursing_care")],
        [InlineKeyboardButton("💊 Clinical Reflection",         callback_data="sample_nursing_reflection")],
        [InlineKeyboardButton("💊 Post-Operative Care Plan",    callback_data="sample_nursing_care_plan")],
        [InlineKeyboardButton("💊 Mental Health Assessment",    callback_data="sample_nursing_mental_health")],
        [InlineKeyboardButton("💊 Safeguarding Children",       callback_data="sample_nursing_safeguarding")],
        [InlineKeyboardButton("💊 Medicines Management",        callback_data="sample_nursing_medicines")],
        [InlineKeyboardButton("💊 End of Life Care",            callback_data="sample_nursing_eol")],
        [InlineKeyboardButton("💊 Dementia Care",               callback_data="sample_nursing_dementia")],
        [InlineKeyboardButton("💊 Infection Control",           callback_data="sample_nursing_infection")],
        [InlineKeyboardButton("💊 Midwifery Practice",          callback_data="sample_nursing_midwifery")],
        [InlineKeyboardButton("💊 Diabetes Management",         callback_data="sample_nursing_diabetes")],
        [InlineKeyboardButton("« Back to Samples",              callback_data="samples")],
    ])

def cs_samples_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💻 Python Programming", callback_data="sample_cs_python")],
        [InlineKeyboardButton("💻 AI/ML Paper",        callback_data="sample_cs_ai")],
        [InlineKeyboardButton("« Back to Samples",     callback_data="samples")],
    ])

def law_samples_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚖️ Criminal Law Essay",      callback_data="sample_law_essay")],
        [InlineKeyboardButton("⚖️ Tort Law Essay",          callback_data="sample_law_tort")],
        [InlineKeyboardButton("⚖️ Contract Law",            callback_data="sample_law_contract")],
        [InlineKeyboardButton("⚖️ Employment Law",          callback_data="sample_law_employment")],
        [InlineKeyboardButton("⚖️ Human Rights Law",        callback_data="sample_law_human_rights")],
        [InlineKeyboardButton("⚖️ Company Law",             callback_data="sample_law_company")],
        [InlineKeyboardButton("⚖️ Land Law",                callback_data="sample_law_land")],
        [InlineKeyboardButton("⚖️ Family Law",              callback_data="sample_law_family")],
        [InlineKeyboardButton("« Back to Samples",          callback_data="samples")],
    ])

def guides_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📖 Harvard Referencing Guide",    callback_data="guide_harvard")],
        [InlineKeyboardButton("📖 APA 7th Edition Guide",        callback_data="guide_apa")],
        [InlineKeyboardButton("📖 OSCOLA Legal Guide",           callback_data="guide_oscola")],
        [InlineKeyboardButton("✏️ How to Write a 2:1 Essay",     callback_data="guide_essay_guide")],
        [InlineKeyboardButton("🎓 Dissertation Success Guide",   callback_data="guide_diss_guide")],
        [InlineKeyboardButton("✅ Turnitin-Safe Guide",           callback_data="guide_turnitin")],
        [InlineKeyboardButton("💊 Nursing Assignments Guide",    callback_data="guide_nursing_guide")],
        [InlineKeyboardButton("🧠 Critical Thinking Guide",      callback_data="guide_critical")],
        [InlineKeyboardButton("« Back to Menu",                  callback_data="main_menu")],
    ])

def services_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Essay Writing",           callback_data="svc_essay")],
        [InlineKeyboardButton("🎓 Dissertation Help",       callback_data="svc_dissertation")],
        [InlineKeyboardButton("📊 Case Studies",            callback_data="svc_case")],
        [InlineKeyboardButton("💊 Nursing Assignments",     callback_data="svc_nursing")],
        [InlineKeyboardButton("⚖️ Law Assignments",         callback_data="svc_law")],
        [InlineKeyboardButton("💼 MBA / Business",          callback_data="svc_mba")],
        [InlineKeyboardButton("💻 Computer Science",        callback_data="svc_cs")],
        [InlineKeyboardButton("🔬 Sciences & Engineering",  callback_data="svc_science")],
        [InlineKeyboardButton("📊 Statistics & Data",       callback_data="svc_stats")],
        [InlineKeyboardButton("🏥 Healthcare & Medicine",   callback_data="svc_health")],
        [InlineKeyboardButton("« Back to Menu",             callback_data="main_menu")],
    ])

def country_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇬🇧 United Kingdom", callback_data="country_uk"),
         InlineKeyboardButton("🇦🇺 Australia",       callback_data="country_au")],
        [InlineKeyboardButton("🇦🇪 UAE",             callback_data="country_uae"),
         InlineKeyboardButton("🇨🇦 Canada",          callback_data="country_ca")],
        [InlineKeyboardButton("🇷🇴 Romania",         callback_data="country_ro"),
         InlineKeyboardButton("🌍 Other",            callback_data="country_other")],
    ])

def back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("« Back to Menu", callback_data="main_menu")]])

def quote_cancel_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("Cancel Quote", callback_data="main_menu")]])

def quote_cta_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Get a Free Quote",  callback_data="quote")],
        [InlineKeyboardButton("📱 WhatsApp Us Now",   url=WHATSAPP_URL)],
        [InlineKeyboardButton("« Back to Menu",       callback_data="main_menu")],
    ])

# ─── HELPERS ───────────────────────────────────────────────────────────────────
async def send_sample(query, sample_key):
    sample = SAMPLES.get(sample_key)
    if sample and not sample["file_id"].startswith(("YOUR_FILE_ID", "PLACEHOLDER")):
        await query.message.reply_document(
            document=sample["file_id"],
            caption=(
                f"📄 *{sample['name']}*"
                f"{STUDY_WARNING}\n\n"
                "Want work of this quality for your own assignment?\n"
                "Get a free quote below 👇"
            ),
            parse_mode="Markdown",
            reply_markup=quote_cta_keyboard()
        )
    else:
        await query.message.reply_text(
            f"📄 *{sample['name']}*\n\n"
            "This sample will be available very soon! In the meantime, "
            "contact us directly and we'll send it to you personally."
            f"{STUDY_WARNING}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📱 WhatsApp Us", url=WHATSAPP_URL)],
                [InlineKeyboardButton("« Back",         callback_data="samples")],
            ])
        )

# ─── WELCOME ───────────────────────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "there"

    welcome = (
        f"👋 *Welcome to AssignPro Solution, {name}!*\n\n"
        "We've helped *18,000+ international students* across the UK, UAE, "
        "Australia, Canada and Romania achieve the grades they deserve.\n\n"
        "✅ 100% AI-free, human-written work\n"
        "✅ Free Turnitin plagiarism report\n"
        "✅ PhD & Master's verified writers\n"
        "✅ Even 6-hour urgent turnarounds\n"
        "✅ Unlimited free revisions\n"
        "✅ Money-back guarantee\n\n"
        "⭐ *4.9/5* from 2,847 real student reviews\n\n"
        "⚠️ *All samples are for STUDY PURPOSES ONLY*\n"
        "Do not copy or submit them as your own work.\n\n"
        "How can we help you today?"
    )
    await update.message.reply_text(
        welcome, parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

    try:
        await ctx.bot.send_message(
            ADMIN_ID,
            f"🔔 New bot user!\n"
            f"Name: {user.full_name}\n"
            f"Username: @{user.username or 'none'}\n"
            f"ID: {user.id}"
        )
    except Exception:
        pass

# ─── MAIN BUTTON HANDLER ───────────────────────────────────────────────────────
async def button_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ── MAIN MENU ──
    if data == "main_menu":
        await query.edit_message_text(
            "Main menu — choose an option below:",
            reply_markup=main_menu_keyboard()
        )

    # ── SAMPLES CATEGORIES ──
    elif data == "samples":
        await query.edit_message_text(
            "📄 *Sample Work*\n\n"
            "All samples are from real orders with grades shown.\n"
            "Choose a category:\n\n"
            f"{STUDY_WARNING}",
            parse_mode="Markdown",
            reply_markup=samples_keyboard()
        )

    elif data == "samples_essays":
        await query.edit_message_text(
            "📝 *Essay Samples*\nChoose a subject:",
            parse_mode="Markdown", reply_markup=essay_samples_keyboard()
        )
    elif data == "samples_dissertations":
        await query.edit_message_text(
            "🎓 *Dissertation Samples*\nChoose a subject:",
            parse_mode="Markdown", reply_markup=dissertation_samples_keyboard()
        )
    elif data == "samples_casestudies":
        await query.edit_message_text(
            "📊 *Case Study Samples*\nChoose a subject:",
            parse_mode="Markdown", reply_markup=case_study_samples_keyboard()
        )
    elif data == "samples_reports":
        await query.edit_message_text(
            "📋 *Report Samples*\nChoose a subject:",
            parse_mode="Markdown", reply_markup=report_samples_keyboard()
        )
    elif data == "samples_literature":
        await query.edit_message_text(
            "📚 *Literature Review Samples*\nChoose a subject:",
            parse_mode="Markdown", reply_markup=literature_samples_keyboard()
        )
    elif data == "samples_nursing":
        await query.edit_message_text(
            "💊 *Nursing Samples*\nChoose a type:",
            parse_mode="Markdown", reply_markup=nursing_samples_keyboard()
        )
    elif data == "samples_cs":
        await query.edit_message_text(
            "💻 *Computer Science Samples*\nChoose a type:",
            parse_mode="Markdown", reply_markup=cs_samples_keyboard()
        )
    elif data == "samples_law":
        await query.edit_message_text(
            "⚖️ *Law Samples*\nChoose a type:",
            parse_mode="Markdown", reply_markup=law_samples_keyboard()
        )

    # ── INDIVIDUAL SAMPLES ──
    elif data == "sample_essay_business":
        await send_sample(query, "essay_business")
    elif data == "sample_essay_marketing":
        await send_sample(query, "essay_marketing")
    elif data == "sample_essay_psychology":
        await send_sample(query, "essay_psychology")
    elif data == "sample_essay_leadership":
        await send_sample(query, "essay_leadership")
    elif data == "sample_essay_hrm":
        await send_sample(query, "essay_hrm")
    elif data == "sample_essay_child_dev":
        await send_sample(query, "essay_child_dev")
    elif data == "sample_essay_economics":
        await send_sample(query, "essay_economics")
    elif data == "sample_essay_public_health":
        await send_sample(query, "essay_public_health")
    elif data == "sample_essay_social_work":
        await send_sample(query, "essay_social_work")
    elif data == "sample_essay_criminology":
        await send_sample(query, "essay_criminology")
    elif data == "sample_essay_media":
        await send_sample(query, "essay_media")
    elif data == "sample_essay_env_law":
        await send_sample(query, "essay_env_law")
    elif data == "sample_essay_education":
        await send_sample(query, "essay_education")
    elif data == "sample_dissertation_nurse":
        await send_sample(query, "dissertation_nurse")
    elif data == "sample_dissertation_mba":
        await send_sample(query, "dissertation_mba")
    elif data == "sample_case_study_law":
        await send_sample(query, "case_study_law")
    elif data == "sample_case_study_mba":
        await send_sample(query, "case_study_mba")
    elif data == "sample_case_study_redbull":
        await send_sample(query, "case_study_redbull")
    elif data == "sample_case_study_cocacola":
        await send_sample(query, "case_study_cocacola")
    elif data == "sample_report_engineering":
        await send_sample(query, "report_engineering")
    elif data == "sample_report_finance":
        await send_sample(query, "report_finance")
    elif data == "sample_report_ml":
        await send_sample(query, "report_ml")
    elif data == "sample_literature_psych":
        await send_sample(query, "literature_psych")
    elif data == "sample_literature_health":
        await send_sample(query, "literature_health")
    elif data == "sample_literature_social":
        await send_sample(query, "literature_social")
    elif data == "sample_nursing_care":
        await send_sample(query, "nursing_care")
    elif data == "sample_nursing_reflection":
        await send_sample(query, "nursing_reflection")
    elif data == "sample_nursing_care_plan":
        await send_sample(query, "nursing_care_plan")
    elif data == "sample_nursing_mental_health":
        await send_sample(query, "nursing_mental_health")
    elif data == "sample_nursing_safeguarding":
        await send_sample(query, "nursing_safeguarding")
    elif data == "sample_nursing_medicines":
        await send_sample(query, "nursing_medicines")
    elif data == "sample_nursing_eol":
        await send_sample(query, "nursing_eol")
    elif data == "sample_nursing_dementia":
        await send_sample(query, "nursing_dementia")
    elif data == "sample_nursing_infection":
        await send_sample(query, "nursing_infection")
    elif data == "sample_nursing_midwifery":
        await send_sample(query, "nursing_midwifery")
    elif data == "sample_nursing_diabetes":
        await send_sample(query, "nursing_diabetes")
    elif data == "sample_cs_python":
        await send_sample(query, "cs_python")
    elif data == "sample_cs_ai":
        await send_sample(query, "cs_ai")
    elif data == "sample_law_essay":
        await send_sample(query, "law_essay")
    elif data == "sample_law_tort":
        await send_sample(query, "law_tort")
    elif data == "sample_law_contract":
        await send_sample(query, "law_contract")
    elif data == "sample_law_employment":
        await send_sample(query, "law_employment")
    elif data == "sample_law_human_rights":
        await send_sample(query, "law_human_rights")
    elif data == "sample_law_company":
        await send_sample(query, "law_company")
    elif data == "sample_law_land":
        await send_sample(query, "law_land")
    elif data == "sample_law_family":
        await send_sample(query, "law_family")

    # ── GUIDES ──
    elif data == "guides":
        await query.edit_message_text(
            "📚 *Free Guides*\n\n"
            "Download these completely free — our gift to every student!\n\n"
            f"{STUDY_WARNING}",
            parse_mode="Markdown",
            reply_markup=guides_keyboard()
        )

    elif data.startswith("guide_"):
        key = data.replace("guide_", "")
        guide = GUIDES.get(key)
        if guide:
            if "YOUR_FILE_ID" not in guide["file_id"]:
                await query.message.reply_document(
                    document=guide["file_id"],
                    caption=(
                        f"📚 *{guide['name']}*\n\n"
                        "100% free from AssignPro Solution.\n"
                        "Need expert help beyond the guide? We're here 24/7."
                        f"{STUDY_WARNING}"
                    ),
                    parse_mode="Markdown",
                    reply_markup=quote_cta_keyboard()
                )
            else:
                await query.message.reply_text(
                    f"📚 *{guide['name']}*\n\n"
                    "This guide is coming very soon! Message us on WhatsApp and we'll send it to you directly.",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("📱 WhatsApp Us", url=WHATSAPP_URL)],
                        [InlineKeyboardButton("« Back",         callback_data="guides")],
                    ])
                )

    # ── PRICING ──
    elif data == "pricing":
        pricing_text = (
            "💰 *Our Pricing*\n\n"
            "Prices depend on subject, deadline and level:\n\n"
            "📌 *Standard (7+ days)*\n"
            "  Undergraduate — from £18/1000 words\n"
            "  Postgraduate  — from £22/1000 words\n"
            "  PhD level     — from £28/1000 words\n\n"
            "⚡ *Urgent (24–48 hours)*\n"
            "  Add 30–50% urgent premium\n\n"
            "🔥 *Rush (6–12 hours)*\n"
            "  Add 60–80% rush premium\n\n"
            "🎁 *First order: use code FIRST20 for 20% off!*\n\n"
            "Every order includes:\n"
            "✅ Free Turnitin plagiarism report\n"
            "✅ Unlimited free revisions\n"
            "✅ Money-back guarantee\n"
            "✅ 100% confidential\n\n"
            "For an exact quote tap below 👇"
        )
        await query.edit_message_text(
            pricing_text, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 Get My Exact Quote", callback_data="quote")],
                [InlineKeyboardButton("📱 WhatsApp Us Now",    url=WHATSAPP_URL)],
                [InlineKeyboardButton("« Back to Menu",         callback_data="main_menu")],
            ])
        )

    # ── REVIEWS ──
    elif data == "reviews":
        reviews_text = (
            "⭐ *What Students Say About Us*\n\n"
            "\"I submitted my nursing dissertation 2 minutes before deadline. "
            "AssignPro saved my degree.\"\n— *Sarah T., Manchester* ⭐⭐⭐⭐⭐\n\n"
            "\"My case study met Harvard Business School format perfectly. Got a 2:1.\"\n"
            "— *James K., Edinburgh* ⭐⭐⭐⭐⭐\n\n"
            "\"International student who didn't understand UK referencing at all. "
            "They walked me through everything.\"\n— *Priya M., UCL* ⭐⭐⭐⭐⭐\n\n"
            "\"Used 3 different services before AssignPro. Wish I found them first.\"\n"
            "— *Ahmed R., Dubai* ⭐⭐⭐⭐⭐\n\n"
            "\"Dissertation submitted on time. First Class. I'm still in shock.\"\n"
            "— *Liu W., Melbourne* ⭐⭐⭐⭐⭐\n\n"
            "\"My law essay had perfect OSCOLA referencing. Got the highest grade in class.\"\n"
            "— *Mohammed A., UAE* ⭐⭐⭐⭐⭐\n\n"
            "\"Ordered a CS programming report — submitted and got 78%. Brilliant.\"\n"
            "— *Raj P., Toronto* ⭐⭐⭐⭐⭐\n\n"
            "\"As a working mum with two kids, I couldn't have passed without them.\"\n"
            "— *Emma B., Birmingham* ⭐⭐⭐⭐⭐\n\n"
            "📊 *4.9/5 average from 2,847 verified reviews*\n"
            "🌍 18,000+ students helped across 8 countries"
        )
        await query.edit_message_text(
            reviews_text, parse_mode="Markdown",
            reply_markup=quote_cta_keyboard()
        )

    # ── SERVICES ──
    elif data == "services":
        await query.edit_message_text(
            "🌍 *Our Services*\n\nSelect a service to learn more:",
            parse_mode="Markdown",
            reply_markup=services_keyboard()
        )

    elif data.startswith("svc_"):
        service_info = {
            "svc_essay":       ("📝 Essay Writing",
                                "Any subject, any level. 500 to 6,000 words. "
                                "Harvard, APA, MLA referencing. 2:1 standard guaranteed."),
            "svc_dissertation":("🎓 Dissertation Help",
                                "Proposal to final submission. Literature review, methodology, "
                                "data analysis, discussion. 5,000 to 15,000+ words."),
            "svc_case":        ("📊 Case Studies",
                                "Business, law, medical, MBA. Real data analysis. "
                                "Structured to your university's marking criteria."),
            "svc_nursing":     ("💊 Nursing Assignments",
                                "NMC standards, clinical reflections, care plans, OSCE reports. "
                                "Expert nursing writers only."),
            "svc_law":         ("⚖️ Law Assignments",
                                "OSCOLA referencing. Case analysis, problem questions, legal essays. "
                                "UK and international law."),
            "svc_mba":         ("💼 MBA / Business",
                                "Business plans, strategy reports, financial analysis, leadership essays. "
                                "Top business school standards."),
            "svc_cs":          ("💻 Computer Science",
                                "Programming assignments, system design, algorithms, AI/ML reports. "
                                "Technical experts only."),
            "svc_science":     ("🔬 Sciences & Engineering",
                                "Lab reports, research papers, technical assignments. STEM-specialist writers."),
            "svc_stats":       ("📊 Statistics & Data Analysis",
                                "SPSS, R, Python, Excel. Quantitative & qualitative analysis. "
                                "Full interpretation included."),
            "svc_health":      ("🏥 Healthcare & Medicine",
                                "Clinical case studies, health policy reports, pharmacology, "
                                "public health assignments. Expert healthcare writers."),
        }
        title, desc = service_info.get(data, ("Service", "Expert help available."))
        await query.edit_message_text(
            f"*{title}*\n\n{desc}\n\n"
            "All orders include:\n"
            "✅ 100% AI-free, human-written\n"
            "✅ Free Turnitin report\n"
            "✅ Unlimited revisions\n"
            "✅ On-time guaranteed\n\n"
            "Get your free quote in 10 minutes 👇",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 Get a Free Quote", callback_data="quote")],
                [InlineKeyboardButton("📱 WhatsApp Us Now",  url=WHATSAPP_URL)],
                [InlineKeyboardButton("« All Services",      callback_data="services")],
            ])
        )

    # ── FAQ ──
    elif data == "faq":
        faq_text = (
            "❓ *Frequently Asked Questions*\n\n"
            "*Is the work AI-generated?*\n"
            "Never. Every word is written by a verified PhD or Master's human expert. "
            "We include a free Turnitin report to prove it.\n\n"
            "*Will it pass Turnitin?*\n"
            "Yes. We include a free plagiarism report with every order. "
            "All work is 100% original.\n\n"
            "*How fast can you deliver?*\n"
            "We can deliver in as little as 6 hours for urgent orders. "
            "Standard is 3–7 days.\n\n"
            "*What if I'm not happy?*\n"
            "Unlimited free revisions until you're satisfied, "
            "or a full money-back guarantee.\n\n"
            "*How do I place an order?*\n"
            "Tap 'Get a Free Quote' below. We'll match you with an expert "
            "and send a quote within 10 minutes.\n\n"
            "*Is it confidential?*\n"
            "100%. We never share your details. Complete privacy guaranteed.\n\n"
            "*Can I get samples before ordering?*\n"
            "Yes! Go to 'View Sample Work' in the main menu.\n\n"
            "*What subjects do you cover?*\n"
            "All subjects — Business, Law, Nursing, CS, Engineering, Psychology, and more."
        )
        await query.edit_message_text(
            faq_text, parse_mode="Markdown",
            reply_markup=quote_cta_keyboard()
        )

    # ── TALK TO HUMAN ──
    elif data == "human":
        await query.edit_message_text(
            "💬 *Talk to Our Team*\n\n"
            "Our experts are online 24/7 and respond in under 10 minutes.\n\n"
            f"📱 *WhatsApp:* +{WHATSAPP_NUM}\n"
            f"🌐 *Website:* {WEBSITE_UK}\n\n"
            "Tap the button below to message us directly on WhatsApp 👇",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📱 WhatsApp Us Now",  url=WHATSAPP_URL)],
                [InlineKeyboardButton("📋 Get a Quote Here", callback_data="quote")],
                [InlineKeyboardButton("« Back to Menu",      callback_data="main_menu")],
            ])
        )

# ─── QUOTE CONVERSATION ────────────────────────────────────────────────────────
async def quote_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            "📋 *Get Your Free Quote*\n\n"
            "I'll get you a price in under 10 minutes.\n"
            "First — which country are you studying in?",
            parse_mode="Markdown",
            reply_markup=country_keyboard()
        )
    return QUOTE_SUBJECT

async def quote_subject(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["subject"] = update.message.text
    await update.message.reply_text(
        "Got it! 📝\n\nWhat's your deadline?\n"
        "_(e.g. 24 hours, 3 days, 1 week, 2 weeks)_",
        parse_mode="Markdown",
        reply_markup=quote_cancel_keyboard()
    )
    return QUOTE_DEADLINE

async def quote_deadline(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["deadline"] = update.message.text
    await update.message.reply_text(
        "Understood ⏰\n\nHow many words do you need?\n"
        "_(e.g. 1000 words, 2500 words, 10000 words)_",
        parse_mode="Markdown",
        reply_markup=quote_cancel_keyboard()
    )
    return QUOTE_WORDS

async def quote_words(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["words"] = update.message.text
    await update.message.reply_text(
        "Perfect! 📊\n\nAny extra details?\n"
        "_(e.g. marking criteria, referencing style, specific requirements — "
        "or just type 'none' to skip)_",
        parse_mode="Markdown",
        reply_markup=quote_cancel_keyboard()
    )
    return QUOTE_DETAILS

async def quote_details(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["details"] = update.message.text
    await update.message.reply_text(
        "Almost done! 🎉\n\n"
        "What's your WhatsApp number or email so we can send you the quote?\n"
        "_(We never share your details — 100% confidential)_",
        parse_mode="Markdown",
        reply_markup=quote_cancel_keyboard()
    )
    return QUOTE_CONTACT

async def quote_contact(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["contact"] = update.message.text
    user = update.effective_user
    d = ctx.user_data

    await update.message.reply_text(
        "✅ *Quote request received!*\n\n"
        "Our team will contact you within *10 minutes* with your exact price.\n\n"
        f"📋 *Your order summary:*\n"
        f"• Country: {d.get('country','Not specified')}\n"
        f"• Subject: {d.get('subject','Not specified')}\n"
        f"• Deadline: {d.get('deadline','Not specified')}\n"
        f"• Word count: {d.get('words','Not specified')}\n"
        f"• Contact: {d.get('contact','Not specified')}\n\n"
        "🎁 Use code *FIRST20* for 20% off your first order!\n\n"
        f"You can also reach us directly on WhatsApp: +{WHATSAPP_NUM}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📱 WhatsApp Us Now", url=WHATSAPP_URL)],
            [InlineKeyboardButton("🏠 Main Menu",       callback_data="main_menu")],
        ])
    )

    try:
        await ctx.bot.send_message(
            ADMIN_ID,
            f"🔥 NEW QUOTE REQUEST!\n\n"
            f"Client: {user.full_name} (@{user.username or 'no username'})\n"
            f"Telegram ID: {user.id}\n\n"
            f"Country:  {d.get('country','?')}\n"
            f"Subject:  {d.get('subject','?')}\n"
            f"Deadline: {d.get('deadline','?')}\n"
            f"Words:    {d.get('words','?')}\n"
            f"Details:  {d.get('details','?')}\n"
            f"Contact:  {d.get('contact','?')}\n\n"
            f"Reply within 10 minutes!"
        )
    except Exception:
        pass

    ctx.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Quote cancelled. Back to the main menu:",
        reply_markup=main_menu_keyboard()
    )
    return ConversationHandler.END

async def country_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    country_map = {
        "country_uk":    ("🇬🇧 United Kingdom", WEBSITE_UK),
        "country_au":    ("🇦🇺 Australia",       WEBSITE_AU),
        "country_uae":   ("🇦🇪 UAE",             WEBSITE_UAE),
        "country_ca":    ("🇨🇦 Canada",           WEBSITE_CA),
        "country_ro":    ("🇷🇴 Romania",          WEBSITE_UK),
        "country_other": ("🌍 International",     WEBSITE_UK),
    }
    label, site = country_map.get(query.data, ("International", WEBSITE_UK))
    ctx.user_data["country"] = label
    ctx.user_data["site"]    = site
    await query.edit_message_text(
        f"Great — {label} selected!\n\n"
        "What subject do you need help with?\n"
        "_(e.g. Business Management, Nursing, Law, Computer Science)_",
        parse_mode="Markdown",
        reply_markup=quote_cancel_keyboard()
    )
    return QUOTE_SUBJECT

# ─── FALLBACK ──────────────────────────────────────────────────────────────────
async def fallback_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # FILE ID HELPER — send a PDF to the bot and it returns the file ID
    if update.message.document:
        file_id = update.message.document.file_id
        file_name = update.message.document.file_name
        await update.message.reply_text(
            f"📄 *File:* {file_name}\n\n🔑 *File ID:*\n`{file_id}`",
            parse_mode="Markdown"
        )
        # Also notify admin
        try:
            await ctx.bot.send_message(
                ADMIN_ID,
                f"📄 File uploaded: {file_name}\nFile ID: {file_id}"
            )
        except Exception:
            pass
    else:
        await update.message.reply_text(
            "Hi! Use the menu below to explore samples, guides, pricing or get a quote:",
            reply_markup=main_menu_keyboard()
        )

# ─── ADMIN BROADCAST ──────────────────────────────────────────────────────────
async def broadcast(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not ctx.args:
        await update.message.reply_text("Usage: /broadcast Your message here")
        return
    msg = " ".join(ctx.args)
    await update.message.reply_text(f"Broadcasting: {msg}")

# ─── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    quote_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(quote_start, pattern="^quote$")],
        states={
            QUOTE_SUBJECT:  [
                CallbackQueryHandler(country_handler, pattern="^country_"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, quote_subject),
            ],
            QUOTE_DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, quote_deadline)],
            QUOTE_WORDS:    [MessageHandler(filters.TEXT & ~filters.COMMAND, quote_words)],
            QUOTE_DETAILS:  [MessageHandler(filters.TEXT & ~filters.COMMAND, quote_details)],
            QUOTE_CONTACT:  [MessageHandler(filters.TEXT & ~filters.COMMAND, quote_contact)],
        },
        fallbacks=[CallbackQueryHandler(cancel, pattern="^main_menu$")],
        per_message=False,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(quote_conv)
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback_message))
    app.add_handler(MessageHandler(filters.Document.ALL, fallback_message))

    print("AssignPro Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()