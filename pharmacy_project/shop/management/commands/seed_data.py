from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Category, Symptom, Medicine


class Command(BaseCommand):
    help = 'Заповнює базу даних тестовими даними'

    def handle(self, *args, **kwargs):
        self.stdout.write('Видалення старих даних...')
        Medicine.objects.all().delete()
        Category.objects.all().delete()
        Symptom.objects.all().delete()

        # Категорії
        categories_data = [
            ('Знеболювальні та протизапальні', 'analgesics'),
            ('Противірусні та імуномодулятори', 'antivirals'),
            ('Антибіотики', 'antibiotics'),
            ('Серцево-судинні', 'cardiovascular'),
            ('Шлунково-кишкові', 'gastrointestinal'),
            ('Вітаміни та мінерали', 'vitamins'),
            ('Антигістамінні', 'antihistamines'),
            ('Неврологічні', 'neurological'),
        ]
        categories = {}
        for name, slug in categories_data:
            c = Category.objects.create(name=name, slug=slug)
            categories[slug] = c
            self.stdout.write(f'  Категорія: {name}')

        # Симптоми
        symptoms_data = [
            ('Головний біль', 'headache'),
            ('Температура', 'fever'),
            ('Кашель', 'cough'),
            ('Нежить', 'runny-nose'),
            ('Біль у горлі', 'sore-throat'),
            ('Нудота', 'nausea'),
            ('Діарея', 'diarrhea'),
            ('Алергія', 'allergy'),
            ('Біль у спині', 'back-pain'),
            ('Безсоння', 'insomnia'),
            ('Слабкість', 'weakness'),
            ('Підвищений тиск', 'high-blood-pressure'),
            ('Зубний біль', 'toothache'),
            ('М\'язовий біль', 'muscle-pain'),
            ('Вірусна інфекція', 'viral-infection'),
        ]
        symptoms = {}
        for name, slug in symptoms_data:
            s = Symptom.objects.create(name=name, slug=slug)
            symptoms[slug] = s

        self.stdout.write(f'  Створено {len(symptoms)} симптомів')

        # Ліки
        medicines_data = [
            {
                'name': 'Нурофен 200 мг',
                'slug': 'nurofen-200',
                'category': 'analgesics',
                'manufacturer': 'Reckitt Benckiser',
                'description': 'Нестероїдний протизапальний препарат на основі ібупрофену. Ефективно знімає біль, жар та запалення.',
                'composition': 'Ібупрофен 200 мг, допоміжні речовини.',
                'dosage': 'Дорослі та діти від 12 років: по 1-2 таблетки кожні 4-6 годин. Не більше 6 таблеток на добу.',
                'contraindications': 'Виразкова хвороба шлунка, порушення згортання крові, вагітність (III триместр).',
                'price': '89.50',
                'stock': 150,
                'is_prescription': False,
                'symptoms': ['headache', 'fever', 'back-pain', 'muscle-pain', 'toothache'],
            },
            {
                'name': 'Парацетамол 500 мг',
                'slug': 'paracetamol-500',
                'category': 'analgesics',
                'manufacturer': 'Дарниця',
                'description': 'Анальгетик та антипіретик. Зменшує температуру і полегшує біль різного походження.',
                'composition': 'Парацетамол 500 мг.',
                'dosage': 'По 1-2 таблетки 3-4 рази на добу. Максимальна добова доза — 4 г.',
                'contraindications': 'Тяжка ниркова або печінкова недостатність, непереносимість парацетамолу.',
                'price': '32.00',
                'stock': 300,
                'is_prescription': False,
                'symptoms': ['headache', 'fever', 'weakness'],
            },
            {
                'name': 'Амоксицилін 500 мг',
                'slug': 'amoxicillin-500',
                'category': 'antibiotics',
                'manufacturer': 'GlaxoSmithKline',
                'description': 'Антибіотик широкого спектру дії з групи амінопеніцилінів. Призначається при бактеріальних інфекціях.',
                'composition': 'Амоксицилін (у вигляді тригідрату) 500 мг.',
                'dosage': 'По 1 капсулі 3 рази на добу кожні 8 годин. Курс — 5-10 днів.',
                'contraindications': 'Алергія на пеніциліни та цефалоспорини. Мононуклеоз.',
                'price': '145.00',
                'stock': 80,
                'is_prescription': True,
                'symptoms': ['fever', 'sore-throat', 'viral-infection'],
            },
            {
                'name': 'Осельтамівір (Таміфлю) 75 мг',
                'slug': 'oseltamivir-75',
                'category': 'antivirals',
                'manufacturer': 'Roche',
                'description': 'Противірусний препарат для лікування та профілактики грипу типів A та B.',
                'composition': 'Осельтамівіру фосфат 98.5 мг (еквівалентно 75 мг осельтамівіру).',
                'dosage': 'Лікування: 75 мг двічі на добу протягом 5 днів. Профілактика: 75 мг один раз на добу 10 днів.',
                'contraindications': 'Ниркова недостатність (потребує корекції дози).',
                'price': '520.00',
                'stock': 40,
                'is_prescription': True,
                'symptoms': ['fever', 'cough', 'weakness', 'viral-infection'],
            },
            {
                'name': 'Лоратадин 10 мг',
                'slug': 'loratadine-10',
                'category': 'antihistamines',
                'manufacturer': 'Здоров\'я',
                'description': 'Антигістамінний препарат тривалої дії. Усуває симптоми алергії без седативного ефекту.',
                'composition': 'Лоратадин 10 мг.',
                'dosage': 'Дорослі та діти від 12 років: 1 таблетка один раз на добу.',
                'contraindications': 'Вагітність (I триместр), годування груддю.',
                'price': '48.00',
                'stock': 200,
                'is_prescription': False,
                'symptoms': ['allergy', 'runny-nose'],
            },
            {
                'name': 'Еналаприл 10 мг',
                'slug': 'enalapril-10',
                'category': 'cardiovascular',
                'manufacturer': 'Фармак',
                'description': 'Інгібітор АПФ. Застосовується для лікування артеріальної гіпертензії та серцевої недостатності.',
                'composition': 'Еналаприлу малеат 10 мг.',
                'dosage': 'Початкова доза 5 мг один раз на добу. Підтримуюча — 10-20 мг.',
                'contraindications': 'Ангіоневротичний набряк в анамнезі, вагітність.',
                'price': '67.50',
                'stock': 120,
                'is_prescription': True,
                'symptoms': ['high-blood-pressure'],
            },
            {
                'name': 'Мезим Форте',
                'slug': 'mezym-forte',
                'category': 'gastrointestinal',
                'manufacturer': 'Berlin-Chemie',
                'description': 'Ферментний препарат, що покращує травлення. Містить панкреатин для розщеплення білків, жирів та вуглеводів.',
                'composition': 'Панкреатин 140 мг (ліпаза 3500 ОД, амілаза 4200 ОД, протеаза 250 ОД).',
                'dosage': 'По 1-3 таблетки під час або після їжі.',
                'contraindications': 'Гострий панкреатит, алергія на свинячий білок.',
                'price': '112.00',
                'stock': 90,
                'is_prescription': False,
                'symptoms': ['nausea'],
            },
            {
                'name': 'Лінекс',
                'slug': 'linex',
                'category': 'gastrointestinal',
                'manufacturer': 'Sandoz',
                'description': 'Пробіотик. Відновлює мікрофлору кишечника після прийому антибіотиків та при кишкових розладах.',
                'composition': 'Ліофілізовані живі молочнокислі бактерії 3 штами.',
                'dosage': 'По 2 капсули 3 рази на день під час їжі.',
                'contraindications': 'Непереносимість лактози, галактоземія.',
                'price': '215.00',
                'stock': 60,
                'is_prescription': False,
                'symptoms': ['diarrhea', 'nausea'],
            },
            {
                'name': 'Вітамін D3 2000 МО',
                'slug': 'vitamin-d3-2000',
                'category': 'vitamins',
                'manufacturer': 'Solgar',
                'description': 'Жиророзчинний вітамін D3 (холекальциферол). Необхідний для засвоєння кальцію та фосфору, підтримки імунітету.',
                'composition': 'Холекальциферол (вітамін D3) 2000 МО.',
                'dosage': 'По 1 таблетці 1 раз на добу під час їжі.',
                'contraindications': 'Гіперкальціємія, саркоїдоз.',
                'price': '289.00',
                'stock': 85,
                'is_prescription': False,
                'symptoms': ['weakness'],
            },
            {
                'name': 'Мелатонін 3 мг',
                'slug': 'melatonin-3',
                'category': 'neurological',
                'manufacturer': 'Evalar',
                'description': 'Синтетичний аналог гормону шишкоподібної залози. Регулює цикл сон-неспання, покращує якість сну.',
                'composition': 'Мелатонін 3 мг.',
                'dosage': 'По 1 таблетці за 30-40 хвилин до сну.',
                'contraindications': 'Аутоімунні захворювання, вагітність, годування груддю.',
                'price': '175.00',
                'stock': 70,
                'is_prescription': False,
                'symptoms': ['insomnia'],
            },
            {
                'name': 'Аугментин 875/125 мг',
                'slug': 'augmentin-875',
                'category': 'antibiotics',
                'manufacturer': 'GlaxoSmithKline',
                'description': 'Комбінований антибіотик (амоксицилін + клавулонова кислота). Ефективний проти стійких до звичайних пеніцилінів бактерій.',
                'composition': 'Амоксицилін 875 мг + клавуланова кислота 125 мг.',
                'dosage': 'По 1 таблетці кожні 12 годин протягом 7-14 днів.',
                'contraindications': 'Алергія на пеніциліни, порушення функції печінки.',
                'price': '310.00',
                'stock': 50,
                'is_prescription': True,
                'symptoms': ['fever', 'sore-throat', 'cough'],
            },
            {
                'name': 'Синупрет краплі',
                'slug': 'sinupret-drops',
                'category': 'antivirals',
                'manufacturer': 'Bionorica',
                'description': 'Рослинний препарат для лікування синуситу та риніту. Має протизапальну та муколітичну дію.',
                'composition': 'Рослинний комплекс: горіан, примула, кислиця, бузина, вербена.',
                'dosage': 'По 50 крапель 3 рази на добу.',
                'contraindications': 'Дитячий вік до 2 років, захворювання печінки.',
                'price': '196.00',
                'stock': 65,
                'is_prescription': False,
                'symptoms': ['runny-nose', 'cough', 'sore-throat'],
            },
        ]

        for data in medicines_data:
            symptom_slugs = data.pop('symptoms')
            cat_slug = data.pop('category')
            data['category'] = categories[cat_slug]
            medicine = Medicine.objects.create(**data)
            for s_slug in symptom_slugs:
                if s_slug in symptoms:
                    medicine.symptoms.add(symptoms[s_slug])
            self.stdout.write(f'  Ліки: {medicine.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nГотово! Створено: {Category.objects.count()} категорій, '
            f'{Symptom.objects.count()} симптомів, {Medicine.objects.count()} препаратів.'
        ))
