from django.core.management.base import BaseCommand
from ...models import Asset, Vol
from datetime import date
from termcolor import colored, cprint
import csv

# python manage.py seed --mode=refresh

# Clear all data
MODE_CLEAR = 'clear'

# Clear all data and repopulate
MODE_REFRESH = 'repopulate'

# Clear all asset data and repopulate assets
MODE_ASSETS = 'assets'

# Clear all vol data and repopulate vol
MODE_VOL = 'vol'

class Command(BaseCommand):
    help = "seed database with data from csv or otherwise"

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def populate_assets():
    Asset.objects.all().delete()
    asset = Asset(
        name = 'S&P 500'        
    )
    asset.save()
    cprint('Saved' + asset.name, 'green')
    return

def populate_vol():
    Vol.objects.all().delete()
    with open('fractal_markets_lab/probability/storage/SPX_volatility.csv', newline = '', encoding='utf-8') as csvfile:
        asset = Asset.objects.get(pk=1)
        reader = csv.DictReader(csvfile)        
        for row in reader:
            # print(row.keys())            
            vol = Vol(
                asset = asset,
                asset_name = asset.name,
                date = row['\ufeffDate'] if row['\ufeffDate'] else '',
                open_price = row['Open'] if row['Open'] else 0,
                close_price = row['Close'] if row['Close'] else 0 ,
                log_returns = row['Log Returns'] if row['Log Returns'] else 0,
                low = row['Low'] if row['Low'] else 0,
                high = row['High'] if row['High'] else 0,
                low_rr = row['LowRR'] if row['LowRR'] else 0,
                high_rr = row['HighRR'] if row['HighRR'] else 0, 
                volatility_index = row['VIX'] if row['VIX'] else 0,
                volume = row['Volume'] if row['Volume'] else 0,
                put_call_ratio = row['PutCall'] if row['PutCall'] else 0,
                vol_stats = {
                        'trade': {
                            'stdev': row['Trade StDev'] if row['Trade StDev'] else 0,
                            'impliedVol': row['Trade IV'] if row['Trade IV'] else 0,
                        },
                        'trend': {
                            'stdev': row['Trend StDev'] if row['Trend StDev'] else 0,
                            'impliedVol': row['Trend IV'] if row['Trend IV'] else 0,
                        },
                        'tail': {
                            'stdev': row['Tail StDev'] if row['Tail StDev'] else 0,
                            'impliedVol': row['Tail IV'] if row['Tail IV'] else 0,
                        }
                    }
                )

            vol.save()
            cprint('Saved row', 'green')
        return

def clear():
    Asset.objects.all().delete()
    Vol.objects.all().delete()
    return


def repopulate():
    Asset.objects.all().delete()
    Vol.objects.all().delete()
    populate_assets()
    populate_vol()
    return


def run_seed(self, mode):
    # Seed database based on mode

    # Clear data from tables and repopulate 
    if mode == MODE_CLEAR:
        clear()
        return

    if mode == MODE_REFRESH:
        repopulate()
        return

    if mode == MODE_ASSETS:
        populate_assets()
        return

    if mode == MODE_VOL:
        populate_vol()
        return


