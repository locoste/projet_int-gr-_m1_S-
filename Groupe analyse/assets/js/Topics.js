var Topics;

function get_Topics_data(){
    httpRequest_topic = new XMLHttpRequest();
    httpRequest_topic.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            response = httpRequest_topic.response;
            script_topic = response.split('<script>')
            script2_topic = script_topic[1].split('</script>')
            document.getElementById('topic').innerHTML += script_topic[0];
            eval(script2_topic[0])

            httpRequest_lda = new XMLHttpRequest();
            httpRequest_lda.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    response = httpRequest_lda.response;
                    script_lda = response.split('<script type="text/javascript">')
                    script2_lda = script_lda[1].split('</script>')
                    document.getElementById('lda').innerHTML += script_lda[0];
                    eval(script2_lda[0])

                    httpRequest_histo = new XMLHttpRequest();
                    httpRequest_histo.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                            response = httpRequest_histo.response;
                            script_histo = response.split('<script>')
                            script2_histo = script_histo[1].split('</script>')
                            document.getElementById('histo').innerHTML += script_histo[0];
                            eval(script2_histo[0])
                                // var topic_value = Topics[document.getElementById('topic_list').value].topic_number
                                // httpRequest_nuage = new XMLHttpRequest();
                                // httpRequest_nuage.onreadystatechange = function() {
                                //     if (this.readyState == 4 && this.status == 200) {
                                //         response = httpRequest_nuage.response;
                                //         script_nuage = response.split('<script>')
                                //         script2_nuage = script_nuage[1].split('</script>')
                                //         document.getElementById('nuage').innerHTML += script_nuage[0] + eval(script2_nuage[0]);
                                //     }
                                // };
                                // httpRequest_nuage.open('GET', 'http://localhost:10546/get_nuage_graph/'+topic_value, false);
                                // httpRequest_nuage.send();
                        }
                    };
                    httpRequest_histo.open('GET', 'http://localhost:10546/get_histo_graph', false);
                    httpRequest_histo.send();
                }
            };
            httpRequest_lda.open('GET', 'http://localhost:10546/get_lda_graph', false);
            httpRequest_lda.send();
        }
    };
    httpRequest_topic.open('GET', 'http://localhost:10546/get_topic_graph', false);
    httpRequest_topic.send();
}

function get_topics_list(){
    httpRequest_topic_list = new XMLHttpRequest();
    httpRequest_topic_list.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            topic_select = document.getElementById('topic_list');
            console.log('topic_list');
            response = JSON.parse(httpRequest_topic_list.response);
            console.log(response);
            Topics = response;
            for(key in response){
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

function get_bag_of_word(){
    var ul = document.getElementById('bag_of_word')
    ul.innerHTML = ""
    console.log(Topics)
    for (i=0; i<Topics[document.getElementById('topic_list').value].bag_of_word.length; i++){
        var li=document.createElement('li');
        li.innerHTML=li.innerHTML + Topics[document.getElementById('topic_list').value].bag_of_word[i];
        ul.appendChild(li);
    }
    var topic_value = Topics[document.getElementById('topic_list').value].topic_number
    httpRequest_nuage = new XMLHttpRequest();
    httpRequest_nuage.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            while(document.getElementById('graph').firstChild) {
                document.getElementById('graph').removeChild(document.getElementById('graph').firstChild);
            }
            response = httpRequest_nuage.response;
            script_nuage = response.split('<script>')
            script2_nuage = script_nuage[1].split('</script>')
            document.getElementById('graph').innerHTML += script_nuage[0]
            eval(script2_nuage[0])
            document.getElementById('graph_title').innerHTML = 'Bag Of Words';
        }
    };
    httpRequest_nuage.open('GET', 'http://localhost:10546/get_nuage_graph/'+topic_value+'?_=' + new Date().getTime(), false);
    httpRequest_nuage.send();
}

function change_label(){
    old_label = document.getElementById('topic_list').value
    var label = prompt("Please enter your name", "Harry Potter");
    if (label != null) {
        httpRequest_change_label = new XMLHttpRequest();
        httpRequest_change_label.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                Topics[label] = Topics[old_label]
                delete Topics[old_label]
                get_topics_list()
            }
        };
        httpRequest_change_label.open('POST', 'http://localhost:10546/set_label', true);
        httpRequest_change_label.send(JSON.stringify({'new_label':label,'bag_of_word':Topics[document.getElementById('topic_list').value]}))
    }
}

function get_topic_graph(){
    var r = confirm("Le traitement va durer plus de 4h.\nVoulez vous continuer?");
    if (r == true) {
        httpRequest_launch_lda = new XMLHttpRequest();
        httpRequest_launch_lda.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                Topics[label] = Topics[old_label]
                console.log(Topics[label])
                delete Topics[old_label]
                get_topics_list()
            }
        };
        httpRequest_launch_lda.open('POST', 'http://localhost:10546/launch_LDA_Treatment', true);
        httpRequest_launch_lda.send()
    }
}


function get_graph(graph){
    var path;
    switch(graph){
        case 'lda':
            path = 'http://localhost:10546/get_lda_graph?_=' + new Date().getTime();
            break;
        case 'score':
            path = 'http://localhost:10546/get_topic_graph?_=' + new Date().getTime();
            break;
        case 'histo':
            path = 'http://localhost:10546/get_histo_graph?_=' + new Date().getTime();
            break;
    }
    httpRequest_graph = new XMLHttpRequest();
    httpRequest_graph.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            switch(graph){
                case 'lda':
                    document.getElementById('graph_title').innerHTML = 'LDA Topics';
                    break;
                case 'score':
                    document.getElementById('graph_title').innerHTML = 'LDA - Coherence Score';
                    break;
                case 'histo':
                    document.getElementById('graph_title').innerHTML = 'Title Number - Topic';
                    break;
            }
            while(document.getElementById('graph').firstChild) {
                document.getElementById('graph').removeChild(document.getElementById('graph').firstChild);
            }
            response = httpRequest_graph.response;
            console.log(response)
            if(graph=='lda'){
                script = response.split('<script type="text/javascript">');
            } else {
                script = response.split('<script>');
            }
            script2 = script[1].split('</script>');
            console.log(script2);
            document.getElementById('graph').innerHTML += script[0];
            eval(script2[0]);
        }
    };
    httpRequest_graph.open('GET', path, true);
    httpRequest_graph.send()
}

get_topics_list();
get_Topics_data();