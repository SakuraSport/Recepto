from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [

        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(
                upload_to='avatars/',
                blank=True,
                null=True
            ),
        ),

        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(
                to=settings.AUTH_USER_MODEL,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='userprofile'
            ),
        ),

        migrations.CreateModel(
            name='Recipe',
            fields=[

                ('id', models.BigAutoField(
                    primary_key=True,
                    serialize=False
                )),

                ('title', models.CharField(
                    max_length=200
                )),

                ('description', models.TextField()),

                ('image', models.ImageField(
                    upload_to='recipes/',
                    blank=True,
                    null=True
                )),

                ('ingredients', models.TextField()),

                ('instructions', models.TextField()),

                ('prep_time', models.IntegerField()),

                ('cook_time', models.IntegerField()),

                ('servings', models.IntegerField()),

                ('difficulty', models.CharField(
                    max_length=10,
                    default='medium'
                )),

                ('views', models.IntegerField(
                    default=0
                )),

                ('likes', models.IntegerField(
                    default=0
                )),

                ('created_at', models.DateTimeField(
                    auto_now_add=True
                )),

                ('updated_at', models.DateTimeField(
                    auto_now=True
                )),

                ('author', models.ForeignKey(
                    to=settings.AUTH_USER_MODEL,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='recipes'
                )),
            ],

            options={
                'ordering': ['-created_at'],
            },
        ),


        migrations.CreateModel(
            name='RecipeLike',
            fields=[

                ('id', models.BigAutoField(
                    primary_key=True,
                    serialize=False
                )),

                ('created_at', models.DateTimeField(
                    auto_now_add=True
                )),

                ('recipe', models.ForeignKey(
                    to='main.recipe',
                    on_delete=django.db.models.deletion.CASCADE
                )),

                ('user', models.ForeignKey(
                    to=settings.AUTH_USER_MODEL,
                    on_delete=django.db.models.deletion.CASCADE
                )),

            ],

            options={
                'unique_together': {
                    ('user', 'recipe')
                }
            },
        ),
    ]