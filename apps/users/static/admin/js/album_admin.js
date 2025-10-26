// Album Admin - Dynamic Music Selection
(function($) {
    'use strict';
    
    $(document).ready(function() {
        var artistField = $('#id_artist');
        
        function loadMusicsForArtist(artistId) {
            if (!artistId) {
                $('#existing_musics').html('Selecione um artista para ver músicas disponíveis');
                return;
            }
            
            // Fazer requisição AJAX para buscar músicas do artista
            $.ajax({
                url: '/api/music/',
                method: 'GET',
                data: {
                    artist: artistId,
                    album__isnull: 'true',
                    is_active: 'true'
                },
                success: function(response) {
                    var musics = response.results || [];
                    
                    if (musics.length === 0) {
                        $('#existing_musics').html('Nenhuma música disponível para este artista');
                        return;
                    }
                    
                    var html = '<div style="max-height: 200px; overflow-y: auto; border: 1px solid #ddd; padding: 10px;">';
                    html += '<strong>Músicas Disponíveis:</strong><br>';
                    html += '<ul style="list-style: none; padding: 0;">';
                    
                    musics.forEach(function(music) {
                        html += '<li style="padding: 5px; border-bottom: 1px solid #eee;">';
                        html += '<strong>' + music.title + '</strong> ';
                        html += '(<a href="/admin/music/music/' + music.id + '/change/" target="_blank">Ver</a>)';
                        html += '</li>';
                    });
                    
                    html += '</ul></div>';
                    $('#existing_musics').html(html);
                },
                error: function() {
                    $('#existing_musics').html('Erro ao carregar músicas');
                }
            });
        }
        
        // Listener para mudança no campo artista
        artistField.on('change', function() {
            var artistId = $(this).val();
            loadMusicsForArtist(artistId);
        });
        
        // Carregar músicas no carregamento inicial se já tem artista selecionado
        if (artistField.val()) {
            loadMusicsForArtist(artistField.val());
        }
    });
})(django.jQuery);

