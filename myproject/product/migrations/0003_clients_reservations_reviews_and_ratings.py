# Generated by Django 5.2 on 2025-04-17 02:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_hotel_rating_room'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname_user', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('name_user', models.CharField(max_length=50, verbose_name='Имя')),
                ('patronymic_user', models.CharField(max_length=50, verbose_name='Отчество')),
                ('email', models.CharField(verbose_name='Email')),
                ('passport_number', models.CharField(max_length=20, unique=True, verbose_name='Паспортные данные')),
                ('address', models.CharField(max_length=50, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Reservations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname_user', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('check_in_date', models.DateField(verbose_name='Дата заезда')),
                ('departure_date', models.DateField(verbose_name='Дата выезда')),
                ('total_amount', models.IntegerField(verbose_name='Общее количество')),
                ('status', models.CharField(choices=[('available', 'Доступно'), ('occupied', 'Занято')], default='available', max_length=10)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.clients')),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.room')),
            ],
            options={
                'verbose_name_plural': 'Отношения',
            },
        ),
        migrations.CreateModel(
            name='Reviews_and_ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname_user', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('estimation', models.IntegerField(verbose_name='Оценка')),
                ('comment', models.CharField(max_length=300, verbose_name='Комментарий')),
                ('date', models.DateField(verbose_name='Дата')),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.clients')),
                ('hotel_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.room')),
            ],
            options={
                'verbose_name_plural': 'Отзывы и оценки',
            },
        ),
    ]
