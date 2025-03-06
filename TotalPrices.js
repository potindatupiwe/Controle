
async function fetchData() {
    const response = await fetch('/graphql/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({
            query: `{
                    totalPrice
                    }`
        })
    });
    const data = await response.json();
    return data.data;
}
async function totaPrice() {
    

const Data = await fetchData();
// Simulação de dados (substituir pelo valor do Django)
const valorTotal = Data.totalPrice; // Exemplo: valor vindo do backen
// Formatação monetária

document.getElementById('valorTotal').textContent = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
}).format(valorTotal);
}
totaPrice();