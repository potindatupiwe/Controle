async function fetchData() {
    const response = await fetch('/graphql/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({
            query: `{
                countBensPorCat{
                    countBens
                    name
                }
                }`
        })
    });
    const data = await response.json();
    return data.data;
}
async function createChartCatCount() {
    const Data = await fetchData();
    
    new Chart(document.getElementById('categoriaChart'), {
        
        type: 'pie',
        data: {
            labels: Data.countBensPorCat.map(cat => cat.name), // Substituir
            datasets: [{
                data: Data.countBensPorCat.map(cat => cat.countBens), // Substituir
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
            }]
        }
    });
}

createChartCatCount()