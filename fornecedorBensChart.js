async function fetchData() {
    const response = await fetch('/graphql/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({
            query: `{
                countFornecedorBens{
                    countBensFornecedor
                    fornecedor
                }
                }`
        })
    });
    const data = await response.json();
    return data.data;
}

async function createChartCatCount() {
    const Data = await fetchData();
    new Chart(document.getElementById('fornecedoresChart'), {
        type: 'bar',
        data: {
            labels: Data.countFornecedorBens.map(fornecedor => fornecedor.fornecedor),
            datasets: [{
                label: 'Ativos Fornecidos',
                data: Data.countFornecedorBens.map(fornecedor => fornecedor.countBensFornecedor), // Substituir
                backgroundColor: '#4BC0C0'
            }]
        },
        options: {
            indexAxis: 'y'
        }
    });
}

createChartCatCount()