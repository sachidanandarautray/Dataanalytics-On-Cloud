document.addEventListener('DOMContentLoaded', () => {
    const extractBtn = document.getElementById('extractBtn');
    const fileInput = document.getElementById('fileInput');
    const tableContainer = document.getElementById('tableContainer');

    extractBtn.addEventListener('click', () => {
        // Implement your logic to extract information from the uploaded file and generate a table
        // Replace this with the code to extract and display the information

        // Example extracted data
        const extractedData = [
            { field: 'Name', value: 'John Doe' },
            { field: 'Email', value: 'johndoe@example.com' },
            // ... other extracted data ...
        ];

        // Generate the table
        const table = document.createElement('table');
        const tableHeader = table.createTHead();
        const row = tableHeader.insertRow();
        const fieldHeader = row.insertCell(0);
        const valueHeader = row.insertCell(1);
        fieldHeader.innerHTML = '<b>Field</b>';
        valueHeader.innerHTML = '<b>Value</b>';

        const tableBody = table.createTBody();
        extractedData.forEach(data => {
            const dataRow = tableBody.insertRow();
            const fieldCell = dataRow.insertCell(0);
            const valueCell = dataRow.insertCell(1);
            fieldCell.textContent = data.field;
            valueCell.textContent = data.value;
        });

        tableContainer.innerHTML = '';
        tableContainer.appendChild(table);
    });

    // Show the selected file name when a file is selected
    fileInput.addEventListener('change', () => {
        const fileName = fileInput.files[0].name;
        const fileLabel = document.querySelector('.file-label');
        fileLabel.textContent = fileName;
    });
});
