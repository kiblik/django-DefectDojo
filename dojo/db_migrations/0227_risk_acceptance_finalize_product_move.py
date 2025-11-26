# Generated migration - Step 3: Finalize Risk_Acceptance move to Product

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0226_risk_acceptance_migrate_to_product'),
    ]

    operations = [
        # Make product field non-nullable
        migrations.AlterField(
            model_name='risk_acceptance',
            name='product',
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='risk_acceptances',
                to='dojo.product'
            ),
        ),

        # Remove the old ManyToMany relationship from Engagement
        migrations.RemoveField(
            model_name='engagement',
            name='risk_acceptance',
        ),
    ]
