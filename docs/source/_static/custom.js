// Make external links open in new tab
document.addEventListener('DOMContentLoaded', function() {
    var links = document.querySelectorAll('a.external, a.reference.external');
    links.forEach(function(link) {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    });
});
