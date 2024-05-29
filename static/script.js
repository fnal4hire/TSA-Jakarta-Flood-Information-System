document.addEventListener("DOMContentLoaded", function() {
    // Function to update the graph image based on selected pintu_air
    window.updatePintuAir = function() {
        const pintuAir = document.getElementById("pintu-air").value;
        const baseUrl = document.querySelector('.dashboard').getAttribute('data-graph-url');
        const graphPath = `${baseUrl}/${pintuAir.replace(' ', '_')}.png`;

        // Update the graph image
        const floodgateGraph = document.getElementById('floodgate-graph');
        floodgateGraph.src = graphPath;
        floodgateGraph.alt = `Graph for ${pintuAir}`;
    };

    // Attach event listener to the select element
    document.getElementById("pintu-air").addEventListener("change", updatePintuAir);
});
