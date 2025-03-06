async function fetchData() {
    const response = await fetch('/graphql/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({
            query: `{
                    bensValor{
                        ativo
                        valor
                    }
                    }`
        })
    });
    const data = await response.json();
    return data.data;
}

async function createChartCatCount() {
    const Data = await fetchData();
    
    const ativos = Data.bensValor.map(ativo => ativo.ativo);
        const valores = Data.bensValor.map(ativo => ativo.valor);

        new Chart(document.getElementById('topAtivosChart'), {
            type: 'bar',
            data: {
                labels: ativos,
                datasets: [{
                    label: 'Valor (R$)',
                    data: valores,
                    backgroundColor: '#2ecc71',
                    borderWidth: 0
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return new Intl.NumberFormat('pt-BR', {
                                    style: 'currency',
                                    currency: 'BRL'
                                }).format(context.raw);
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return new Intl.NumberFormat('pt-BR', {
                                    style: 'currency',
                                    currency: 'BRL'
                                }).format(value);
                            }
                        }
                    }
                }
            }
        });
}

createChartCatCount()