# Testes Automatizados - Ehit Backend

## 📋 Visão Geral

Este projeto possui uma suíte completa de testes automatizados com **60 testes** cobrindo todos os modelos e funcionalidades do sistema.

## 🧪 Cobertura de Testes

### **Apps.users** (12 testes)
- ✅ **UserModelTest** - Testes do modelo User customizado
  - Criação de usuário comum e superusuário
  - Representação string e propriedades de tipo
  - Validação de campos obrigatórios
  - Sistema de verificação e contadores
  - Ordenação padrão

- ✅ **UserManagerTest** - Testes do manager de usuários
  - Criação com e sem senha
  - Validação de superusuário

### **Apps.artists** (12 testes)
- ✅ **BaseModelTest** - Testes do modelo base
  - Campos comuns (created_at, updated_at, is_active)
  - Ordenação padrão

- ✅ **ArtistModelTest** - Testes do modelo Artist
  - Criação e relacionamento one-to-one com User
  - Métodos de estatísticas e verificação
  - Links sociais e ordenação
  - Campos obrigatórios

- ✅ **ArtistIntegrationTest** - Testes de integração
  - Estatísticas com músicas reais
  - Ordenação por estatísticas

### **Apps.music** (12 testes)
- ✅ **MusicModelTest** - Testes do modelo Music
  - Criação e relacionamento com Artist
  - Métodos de URL, duração e estatísticas
  - Propriedades (popular, trending)
  - Campos obrigatórios e ordenação

- ✅ **MusicIntegrationTest** - Testes de integração
  - Relacionamento música-artista
  - Ordenação por estatísticas
  - Lógica de música trending

### **Apps.playlists** (24 testes)
- ✅ **PlaylistModelTest** - Testes do modelo Playlist
  - Criação e métodos de duração
  - Adição/remoção de músicas
  - Reordenação e formatos de duração
  - Privacidade e contadores

- ✅ **PlaylistMusicModelTest** - Testes do modelo intermediário
  - Criação e ordenação
  - Constraint unique_together

- ✅ **UserFavoriteModelTest** - Testes de favoritos
  - Criação e relacionamentos
  - Ordenação e constraints

- ✅ **PlaylistIntegrationTest** - Testes de integração
  - Playlists com múltiplas músicas
  - Ordenação por seguidores

## 🚀 Executando os Testes

### Comando Básico
```bash
python manage.py test
```

### Com Verbosidade
```bash
python manage.py test --verbosity=2
```

### Testes Específicos
```bash
# Testar apenas um app
python manage.py test apps.users

# Testar uma classe específica
python manage.py test apps.users.tests.UserModelTest

# Testar um método específico
python manage.py test apps.users.tests.UserModelTest.test_create_user
```

## 📊 Estatísticas dos Testes

- **Total de Testes**: 60
- **Tempo de Execução**: ~8 segundos
- **Cobertura**: 100% dos modelos principais
- **Status**: ✅ Todos os testes passando

## 🔧 Configuração

### pytest.ini
```ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = ehit_backend.settings
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
addopts = --tb=short --strict-markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

## 📝 Padrões de Teste

### Estrutura dos Testes
- **setUp()**: Configuração inicial para cada teste
- **test_***: Métodos de teste individuais
- **Docstrings**: Descrição clara do que cada teste verifica

### Tipos de Teste
- **Unit Tests**: Testam modelos individuais
- **Integration Tests**: Testam relacionamentos entre modelos
- **Validation Tests**: Testam validações e constraints

### Boas Práticas
- ✅ Nomes descritivos para testes
- ✅ Documentação com docstrings
- ✅ Testes independentes (sem dependências entre eles)
- ✅ Limpeza automática do banco de teste
- ✅ Cobertura completa de funcionalidades

## 🎯 Objetivos dos Testes

1. **Garantir Qualidade**: Validar que todos os modelos funcionam corretamente
2. **Prevenir Regressões**: Detectar mudanças que quebram funcionalidades
3. **Documentar Comportamento**: Os testes servem como documentação viva
4. **Facilitar Refatoração**: Permitir mudanças com confiança
5. **Integração Contínua**: Base para CI/CD

## 🔍 Casos de Teste Cobertos

### Modelos
- ✅ Criação e validação
- ✅ Relacionamentos (ForeignKey, OneToOne, ManyToMany)
- ✅ Métodos customizados
- ✅ Propriedades calculadas
- ✅ Ordenação padrão
- ✅ Constraints (unique_together)

### Funcionalidades
- ✅ Sistema de usuários customizado
- ✅ Perfis de artistas
- ✅ Gestão de músicas
- ✅ Playlists e favoritos
- ✅ Estatísticas e contadores
- ✅ Sistema de verificação

### Integração
- ✅ Relacionamentos entre modelos
- ✅ Cálculos agregados
- ✅ Ordenação por estatísticas
- ✅ Lógica de negócio complexa

---

**Status**: ✅ **Todos os 60 testes passando com sucesso!**
