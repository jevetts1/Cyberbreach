$(document).ready(function () {
  // latest full node list
  var fullNodeList;

  /**
   * Listen to when network is updated in the network editor
   */
  $(document).on('updateNodeList', (nodeList) => updateNodeList(nodeList?.detail));

  /**
   * Listen to filter inputs
   */
  $('#node-list-filter').keyup(function () {
    let input = this;
    // filter node list by name
    updateNodeList(fullNodeList, $(input).val())
  });

  $('#node-list-filter').on("search", function () {
    // load the full node list
    updateNodeList(fullNodeList, null);
  });

  /**
 * Update the node list container with the latest node list
 * @param {*} nodeList 
 * @returns 
 */
  function updateNodeList(nodeList, filterStr) {
    var nodeListContainer = $("#node-list-container");

    // make sure that the node list is an iterable array
    if (!nodeList || !Array.isArray(nodeList) || !nodeList.length) {
      return;
    }

    // save the list
    fullNodeList = nodeList;

    // clear the list
    nodeListContainer.empty();

    // filter array if there is a filter
    if (!!filterStr && !!filterStr.trim()) {
      nodeList = nodeList.filter(node => node?.name.indexOf(filterStr) > -1)
    }

    // sort by name
    nodeList.sort((a, b) => {
      if (a.name < b.name)
        return -1;
      if (a.name > b.name)
        return 1;
      return 0;
    }).forEach(node => {
      // add the node list item to the node lsit container
      nodeListContainer.append(createNodeListItem(node.uuid, node.name));
    });
  }

  /**
   * Creates the node list item element
   * @param {*} id 
   * @param {*} name 
   * @returns 
   */
  function createNodeListItem(id, name) {
    // create node list container
    var nodeListItem = document.createElement("div");
    nodeListItem.id = id;
    nodeListItem.classList.add('node-list-item');

    // create node list text
    var nodeListItemLabel = document.createElement("div");
    nodeListItemLabel.innerHTML = name;
    nodeListItemLabel.classList.add('node-list-item-label');
    nodeListItem.appendChild(nodeListItemLabel);

    // create node list button
    var nodeListDeleteIconButton = document.createElement("button");
    nodeListDeleteIconButton.classList.add("btn");
    nodeListDeleteIconButton.id = id;
    var nodeListDeleteIcon = document.createElement("i");
    nodeListDeleteIcon.classList.add("bi");
    nodeListDeleteIcon.classList.add("bi-x-lg");
    nodeListDeleteIconButton.appendChild(nodeListDeleteIcon);
    nodeListItem.appendChild(nodeListDeleteIconButton);

    return nodeListItem;
  }
})
