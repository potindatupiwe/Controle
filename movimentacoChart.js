async function fetchData() {
    const response = await fetch('/graphql/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({
            query: `{
                countMoveMes{
                    countMes
                    numMes
                }
                }`
        })
    });
    const data = await response.json();
    return data.data;
}
async function createChartCatCount() {
    const Data = await fetchData();
new Chart(document.getElementById('movimentacoesChart'), {
    type: 'line',
    data: {
        labels: ['Jan', 'Fev', 'Mar', 'Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'], // Substituir por datas
        datasets: [{
            label: 'Movimentações',
            data: Data.countMoveMes.map(move => move.countMes),
            borderColor: '#36A2EB',
            tension: 0.4
        }]
    }
});

}

createChartCatCount()