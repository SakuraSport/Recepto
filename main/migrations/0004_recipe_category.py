

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_userprofile_verification_token'),
    ]
    # Это поисковик
    operations = [
        migrations.AddField(
            model_name='recipe',
            name='category',
            field=models.CharField(choices=[('breakfast', 'Завтрак'), ('lunch', 'Обед'), ('dinner', 'Ужин'), ('dessert', 'Десерт'), ('drink', 'Напиток'), ('snack', 'Закуска')], default='lunch', max_length=20),
        ),
    ]
