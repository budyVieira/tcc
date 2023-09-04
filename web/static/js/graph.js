var ctx = document.getElementById('myChart').getContext('2d');

// Use as variáveis Jinja2 para os rótulos e dados
var labels = {{ labels|tojson }};
var data = {{ data|tojson }};

var chartData = {
    labels: labels,
    datasets: [{
        label: 'Quantidade de Ocorrências',
        data: data,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
    }]
};

var myChart = new Chart(ctx, {
    type: 'bar',
    data: chartData
});