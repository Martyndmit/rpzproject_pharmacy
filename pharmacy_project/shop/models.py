from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва')
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, verbose_name='Опис')

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:catalog') + f'?category={self.slug}'


class Symptom(models.Model):
    name = models.CharField(max_length=200, verbose_name='Симптом')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Симптом'
        verbose_name_plural = 'Симптоми'
        ordering = ['name']

    def __str__(self):
        return self.name


class Medicine(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='medicines', verbose_name='Категорія'
    )
    symptoms = models.ManyToManyField(
        Symptom, blank=True,
        related_name='medicines', verbose_name='Симптоми'
    )
    name = models.CharField(max_length=300, verbose_name='Назва')
    slug = models.SlugField(max_length=300, unique=True)
    manufacturer = models.CharField(max_length=200, blank=True, verbose_name='Виробник')
    description = models.TextField(verbose_name='Опис')
    composition = models.TextField(blank=True, verbose_name='Склад')
    dosage = models.CharField(max_length=200, blank=True, verbose_name='Дозування')
    contraindications = models.TextField(blank=True, verbose_name='Протипоказання')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна (грн)')
    stock = models.PositiveIntegerField(default=0, verbose_name='Залишок на складі')
    is_prescription = models.BooleanField(default=False, verbose_name='Рецептурний препарат')
    is_available = models.BooleanField(default=True, verbose_name='Доступний')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ліки'
        verbose_name_plural = 'Ліки'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:medicine_detail', args=[self.slug])


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В обробці'),
        ('confirmed', 'Підтверджено'),
        ('shipping', 'Доставляється'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Скасовано'),
    ]

    DELIVERY_CHOICES = [
        ('nova_poshta', 'Нова Пошта'),
        ('ukrposhta', 'Укрпошта'),
        ('courier', 'Кур\u2019єр по місту'),
        ('pickup', 'Самовивіз'),
    ]

    first_name = models.CharField(max_length=100, verbose_name='Ім\'я')
    last_name = models.CharField(max_length=100, verbose_name='Прізвище')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    delivery_method = models.CharField(
        max_length=20, choices=DELIVERY_CHOICES,
        default='nova_poshta', verbose_name='Спосіб доставки'
    )
    address = models.CharField(max_length=300, verbose_name='Адреса / відділення')
    city = models.CharField(max_length=100, verbose_name='Місто')
    has_prescription = models.BooleanField(
        default=False, verbose_name='Наявний рецепт'
    )
    prescription_note = models.TextField(
        blank=True, verbose_name='Примітка щодо рецепту'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='pending', verbose_name='Статус'
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0, verbose_name='Загальна сума'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата замовлення')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created']

    def __str__(self):
        return f'Замовлення #{self.id} — {self.last_name} {self.first_name}'

    def get_total(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='items', verbose_name='Замовлення'
    )
    medicine = models.ForeignKey(
        Medicine, on_delete=models.PROTECT,
        related_name='order_items', verbose_name='Ліки'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кількість')

    class Meta:
        verbose_name = 'Позиція замовлення'
        verbose_name_plural = 'Позиції замовлення'

    def __str__(self):
        return f'{self.medicine.name} x{self.quantity}'

    def get_cost(self):
        return self.price * self.quantity
