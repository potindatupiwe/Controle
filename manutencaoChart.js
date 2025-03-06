async function fetchData() {
    const response = await fetch('/graphql/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({
            query: `{
                countBensStatus{
                    countStatus
                    nameStatus
                }
                }`
        })
    });
    const data = await response.json();
    return data.data;
}
async function createChartCatCount() {
    const Data = await fetchData();
    new Chart(document.getElementById('manutencaoChart'), {
        type: 'doughnut',
        data: {
            labels: Data.countBensStatus.map(ativo => ativo.nameStatus),
            datasets: [{
                data: Data.countBensStatus.map(ativo => ativo.countStatus), // Substituir
                backgroundColor: ['#FF6384', '#FF9F40', '#4BC0C0']
            }]
        }
    });
}

createChartCatCount()