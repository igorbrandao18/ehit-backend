"""
Comando Django para gerenciar cache Redis
"""
from django.core.management.base import BaseCommand
from django.core.cache import cache
from apps.cache_utils import clear_all_cache, warm_up_cache, get_cache_stats


class Command(BaseCommand):
    help = 'Gerenciar cache Redis da aplicação'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=['clear', 'warm', 'stats', 'test'],
            help='Ação a ser executada: clear (limpar), warm (aquecer), stats (estatísticas), test (testar)'
        )

    def handle(self, *args, **options):
        action = options['action']
        
        if action == 'clear':
            self.clear_cache()
        elif action == 'warm':
            self.warm_cache()
        elif action == 'stats':
            self.show_stats()
        elif action == 'test':
            self.test_cache()

    def clear_cache(self):
        """Limpar todo o cache"""
        self.stdout.write('🧹 Limpando cache Redis...')
        try:
            clear_all_cache()
            self.stdout.write(
                self.style.SUCCESS('✅ Cache limpo com sucesso!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao limpar cache: {e}')
            )

    def warm_cache(self):
        """Aquecer cache com dados frequentes"""
        self.stdout.write('🔥 Aquecendo cache Redis...')
        try:
            warm_up_cache()
            self.stdout.write(
                self.style.SUCCESS('✅ Cache aquecido com sucesso!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao aquecer cache: {e}')
            )

    def show_stats(self):
        """Mostrar estatísticas do cache"""
        self.stdout.write('📊 Estatísticas do cache Redis:')
        try:
            stats = get_cache_stats()
            for key, value in stats.items():
                self.stdout.write(f'  {key}: {value}')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao obter estatísticas: {e}')
            )

    def test_cache(self):
        """Testar funcionalidade do cache"""
        self.stdout.write('🧪 Testando cache Redis...')
        try:
            # Teste básico
            test_key = 'test_cache_key'
            test_value = 'test_value_123'
            
            # Salvar no cache
            cache.set(test_key, test_value, 60)
            self.stdout.write('  ✅ Escrita no cache: OK')
            
            # Ler do cache
            cached_value = cache.get(test_key)
            if cached_value == test_value:
                self.stdout.write('  ✅ Leitura do cache: OK')
            else:
                self.stdout.write('  ❌ Leitura do cache: FALHOU')
                return
            
            # Deletar do cache
            cache.delete(test_key)
            deleted_value = cache.get(test_key)
            if deleted_value is None:
                self.stdout.write('  ✅ Deleção do cache: OK')
            else:
                self.stdout.write('  ❌ Deleção do cache: FALHOU')
                return
            
            self.stdout.write(
                self.style.SUCCESS('✅ Teste do cache concluído com sucesso!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro no teste do cache: {e}')
            )
