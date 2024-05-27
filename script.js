document.addEventListener("DOMContentLoaded", function() {
    const pintuAirSelector = document.getElementById('pintu-air');
    pintuAirSelector.addEventListener('change', function() {
        const selectedPintuAir = pintuAirSelector.value;
        updateFloodgateGraph(selectedPintuAir);
        updateFloodgateTable(selectedPintuAir);
    });

    function updateFloodgateGraph(pintuAir) {
        const graphImg = document.getElementById('floodgate-graph');
        graphImg.src = `/floodgate_graph/${encodeURIComponent(pintuAir)}`;
    }

    function updateFloodgateTable(pintuAir) {
        axios.get('/floodgate_table')
            .then(response => {
                document.getElementById('floodgate-table').innerHTML = response.data;
            })
            .catch(error => {
                console.error('Error fetching floodgate table:', error);
            });
    }

    // Initial load
    const initialPintuAir = pintuAirSelector.value;
    updateFloodgateGraph(initialPintuAir);
    updateFloodgateTable(initialPintuAir);
});