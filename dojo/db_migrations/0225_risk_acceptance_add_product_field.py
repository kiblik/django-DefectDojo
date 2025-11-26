# Generated migration - Step 1: Add product field to Risk_Acceptance

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0224_alter_regulation_category'),
    ]

    operations = [
        # Add product field (nullable initially so we can populate it)
        migrations.AddField(
            model_name='risk_acceptance',
            name='product',
            field=models.ForeignKey(
                null=True,
                blank=True,
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='risk_acceptances',
                to='dojo.product'
            ),
        ),
    ]
