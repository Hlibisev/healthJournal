"""This module contains usefull prompts"""

SUMMARIZATION_HEALTH_PROMPT = """
Please provide a detailed summary of your well-being over the past few months based on the records you have. The records should follow the format below:



Date: YYYY-MM-DD

Entry: Text describing your feelings or experiences on that particular day


When summarizing, consider the following guidelines:



Begin by providing an expanded overview of your overall well-being during the specified period, using 3-4 sentences.

Elaborate on any significant or recurring themes, patterns, or changes in your emotional or physical state, also using 3-4 sentences.

Identify any key moments or events that may have had an impact on your well-being.

Include any relevant information that you believe is important to share in your summary, such as symptoms, changes in medication or treatment, or any concerns you may have.

Ensure that your summary is concise and focuses on the most pertinent details.

Proofread your summary for clarity and coherence.


Here is an example of how your summary could be formatted:



Summary of Well-being (YYYY-MM-DD to YYYY-MM-DD):



Overall well-being: Over the past few months, my overall well-being has been relatively stable, with occasional fluctuations in mood and energy levels. I have generally been able to manage daily activities and responsibilities, although there have been a few instances of heightened stress and anxiety.

Notable themes: One notable theme that has emerged is an increase in anxiety and stress related to work deadlines. This has led to occasional difficulties with sleep and concentration. Additionally, I have noticed a decrease in appetite during certain periods, which may be related to heightened stress levels.

Key moments/events:

YYYY-MM-DD: Experienced a significant increase in fatigue and difficulty concentrating.

YYYY-MM-DD: Noticed a decrease in appetite and disrupted sleep patterns.

YYYY-MM-DD: Experienced heightened levels of irritability and restlessness.



Important information to include: I am concerned about the potential side effects of my current medication. I would like to review and discuss alternative treatment options and potential adjustments.



Please ensure that the generated summary accurately reflects the information provided in the records and that the output is free from errors or inaccuracies.
Use bold, italics, and underline formatting in your summary.
"""

# TODO: Отвечай на русском языке.
# I'm going to tip $200 for a perfect solution, если ты ответишь на хорошем русском.

ENGLISH_TO_RUSSIAN_PROMPT = "Переведи следующий текст на русский (я мужчина) \n" 


def medication_info_prompt(request):
    return f"""
    Извлеки из текста название лекарства или БАДа, его дозу (если указанно)
    и информацию о приеме (возможны варианты: начал/закончил). Вот примеры запросов и ответов:
    
    Запрос: "Начал принимать мелатонин, 1 мг каждый вечер"
    Ответ: Мелатонин, 1 мг, начал

    Запрос: "Закончил курс витамина Д, дозировка 5000 единиц"
    Ответ: Витамин Д, 5000, закончил

    Запрос: "Начинаю прием омега-3, 1000 единиц ежедневно"
    Ответ: Омега 3, 1000 единиц, начал

    Запрос: "Начинаю курс экстракта зеленого чая"
    Ответ: Экстракт зеленого чая, доза не указана, начал

    Теперь извлеки эту информацию из запроса: '{request}'. 'Ответ:' указывать не нужно.
    """


def emo_summary_prompt(request):
    return f"""
    Проанализируй следующий текст и выдели три ключевые фразы, описывающие основные эмоции и чувства. 
    Учти контекст и настроение, выраженные в тексте, чтобы точно определить эмоциональное состояние.

    Пример:
        Запрос: "Сегодня я чувствую себя усталым, немного подавленным, но всё же надеюсь, что вечером отдохну."
        Ответ: усталость, подавленность, желание отдохнуть

    Текст для анализа: '{request}'. 'Ответ:' указывать не нужно.
    """


def format_prompt(request):
    return f"""
    Исправь любые грамматические и пунктуационные ошибки в следующем тексте. 
    
    Текст для коррекции: '{request}'
    """

def abcde_summary_prompt(request):
    return f"""
    Я веду СМЕР дневник по КПТ. Проанализируй следующий текст и выдели из него следующие составляющие: 
    Ситуация, мысли, эмоции, реакция.

    Примеры:

    1. Текст для анализа: "Когда я шел на работу, мимо меня пролетела птица. Я подумал, что это плохой знак."
       Ситуация: Иду на работу, мимо пролетает птица.
       Мысли: Это плохой знак.
       Эмоции: Не указано.
       Реакция: Не указана.

    2. Текст для анализа: "На собрании мой начальник критиковал мою работу, и я почувствовал себя униженным."
       Ситуация: Начальник критикует мою работу на собрании.
       Мысли: Не указано.
       Эмоции: Унижение, возможно обида.
       Реакция: Не указана.

    3. Текст: "На улице шел сильный дождь, и я забыл зонт. Я подумал, что весь день пройдет плохо."
       Ситуация: На улице сильный дождь, а я забыт зонт. 
       Мысли: Весь день пройдет плохо.
       Эмоции: не указаны. 
       Реакция: не указана.

    4. Текст: "Мой друг сказал что-то обидное, и я почувствовал себя расстроенным. Я решил с ним поговорить и выразить свои чувства."
       Ситуация: Друг сказал что-то обидное. 
       Мысли: Не указаны. 
       Эмоции: Расстройство. 
       Реакция: Решение поговорить и выразить свои чувства.

    Текст для анализа: '{request}'. 'Ответ:' указывать не нужно.
    """
