async function fetchData() {
    const response = await fetch('/graphql/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({
            query: `{
                countBensDpt{
                    countBens
                    dpt
                }
                }`
        })
    });
    const data = await response.json();
    return data.data;
}

async function createChartCatCount() {
    const Data = await fetchData();
    new Chart(document.getElementById('departamentoChart'), {
        type: 'bar',
        data: {
            labels: Data.countBensDpt.map(dept => dept.dpt), // Substituir
            datasets: [{
                label: 'Quantidade de Ativos',
                data: Data.countBensDpt.map(dept => dept.countBens), // Substituir
                backgroundColor: '#FF9F40'
            }]
        }
    });
}

createChartCatCount()