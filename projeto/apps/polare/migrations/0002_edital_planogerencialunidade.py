# Generated by Django 4.2.2 on 2023-07-04 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polare', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edital',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('ativo', models.BooleanField()),
                ('versao', models.BigIntegerField()),
                ('data_fim', models.DateTimeField()),
                ('data_fim_inscricao', models.DateTimeField(blank=True, null=True)),
                ('data_inicio', models.DateTimeField()),
                ('data_inicio_inscricao', models.DateTimeField(blank=True, null=True)),
                ('id_arquivo', models.BigIntegerField(blank=True, null=True)),
                ('link_edital', models.CharField(blank=True, max_length=255, null=True)),
                ('numero', models.BigIntegerField()),
                ('resumo', models.TextField()),
                ('titulo', models.CharField(max_length=255)),
                ('vagas', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'polare"."edital',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlanoGerencialUnidade',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('ativo', models.BooleanField()),
                ('versao', models.BigIntegerField()),
                ('ano_referencia', models.BigIntegerField()),
                ('atribuicoes', models.TextField()),
                ('siape_responsavel', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'polare"."plano_gerencial_unidade',
                'managed': False,
            },
        ),
    ]
