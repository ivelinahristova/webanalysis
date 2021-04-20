d3.json('/sources', function (error, sources) {
    var charts = document.getElementById('social_charts');
    var uri = charts.getAttribute('data-url')
    sources.forEach(function (source) {
        img = document.createElement('img')
        img.src = uri + source + '.png'
        charts.append(img)
    });
});