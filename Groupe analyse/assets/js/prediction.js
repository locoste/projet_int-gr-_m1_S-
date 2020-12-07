var topic_list;


function get_prediction_data(){
    httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            response = httpRequest.response;
            while(document.getElementById('prediction_chart').firstChild) {
                document.getElementById('prediction_chart').removeChild(document.getElementById('prediction_chart').firstChild);
            }
            // div = document.createElement('div');
            // div.innerHTML = response;
            // document.getElementById('prediction_chart').appendChild(div);
            script = response.split('<script>')
            script2 = script[1].split('</script>')
            console.log(script[0])
            document.getElementById('prediction_chart').innerHTML =script[0]
            eval(script2[0]);
            console.log(document.getElementById('prediction_chart'))
        }
    };
    console.log('http://localhost:10546/get_prediction_graph/'+topic_list[document.getElementById('topic_list').value].topic_number)
    httpRequest.open('GET', 'http://localhost:10546/get_prediction_graph/'+topic_list[document.getElementById('topic_list').value].topic_number, true);
    httpRequest.send();
}

function get_topics_list(){
    httpRequest_topic_list = new XMLHttpRequest();
    httpRequest_topic_list.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            topic_select = document.getElementById('topic_list');
            console.log('topic_list');
            topic_list = JSON.parse(httpRequest_topic_list.response);
            bag_of_word = topic_list;
            for(key in topic_list){
                var option = document.createElement("option");
                option.text = key;
                option.value = key;
                // option.onclick = "get_bag_of_word(key)";
                topic_select.add(option, topic_select[1]);
            }
        }
    };
    httpRequest_topic_list.open('GET', 'http://localhost:10546/get_topic_list', true);
    httpRequest_topic_list.send();
}

get_topics_list();