const searchField = document.querySelector('#SearchField');
const tableOutput = document.querySelector('.table-output');
const appTable = document.querySelector('.app-table');
const paginationContainer = document.querySelector('.pagination-container');
const tablebody = document.querySelector('.table-body');

tableOutput.style.display ='none';

searchField.addEventListener('keyup',(e) =>{
    const searchValue = e.target.value;

    if(searchValue.trim().length > 0){
        console.log('searchValue',searchValue)
        paginationContainer.style.display = 'none';
         
        tablebody.innerHTML = "";
        fetch("/search_text",{
            body:JSON.stringify({searchText:searchValue}),
            method:"POST",
        })
        .then((res)=> res.json())
        .then((data)=>{
            // console.log("data:",data);
            appTable.style.display = 'none';
            tableOutput.style.display ='block';
            if(data.length === 0){
                tableOutput.innerHTML ="No results found!";
                
            }
            else{
                data.forEach(element => {
                    tablebody.innerHTML +=`
                    <tr>
                    <td>${element.amount}</td>
                    <td>${element.category}</td>
                    <td>${element.description}</td>
                    <td>${element.date}</td>
                    <td></td>
                    </tr>`;
                   
                    
                });
            }
            
        });

    }else{
        paginationContainer.style.display = 'block';
        appTable.style.display = 'block';
        tableOutput.style.display ='none';

    }


})