import QtQuick 2.0
Rectangle {
    id: button0
    width:920
    height:520
    ListView {
        id: pythonTopList
        x:20
        y:10
        width:920
        height:260
        spacing: 20

        model: pythonListModel1
        orientation: Qt.Horizontal

        delegate: Rectangle {
            id: auction
            width: 160
            height: 240
            color:"#D5D5D5"

            Rectangle {
                id: image
                x: 0
                y: 0
                width: 160
                height: 160
                color:"#D5D5D5"
                Image {
                    id: image1
                    x: 0
                    y: 0
                    width: 160
                    height: 160
                    fillMode: Image.PreserveAspectFit
                    smooth: true
                    source: model.auction.thumbnailpath
                }
            }
            Rectangle {
                id: namebg
                x: 0
                y: 160
                width: 160
                height: 20
                color:"black"
                Text {
                    id: name
                    x: 4
                    y: 0
                    width: 152
                    height: 20
                    text: qsTr(model.auction.name)
                    verticalAlignment :Text.AlignVCenter
                    font.pixelSize: 14
                    color:"lightgray"
                    font.family: "Calibri"
                    wrapMode: "WrapAnywhere"
                }
            }


            Text {
                id: buyoutprice
                x: 0
                y: 185
                width: 80
                height: 20
                horizontalAlignment :Text.AlignHCenter
                text: qsTr(model.auction.buyoutprice)
                font.pixelSize: 14
                font.family: "Calibri"
            }

            Rectangle {
                id: buy
                x: 7
                y: 209
                width: 70
                height: 23
                color:"#EA0000"
                Text {
                    id: text7
                    x: 0
                    y: 0
                    width: 70
                    height: 20
                    text: qsTr("Buy")
                    horizontalAlignment :Text.AlignHCenter
                    verticalAlignment :Text.AlignVCenter

                    font.pixelSize: 14
                    color:"#F9F9F9"
                    font.bold : true
                    font.family: "Calibri"

                }
            }

            Text {
                id: bidprice
                x: 80
                y: 185
                width: 80
                height: 20
                horizontalAlignment :Text.AlignHCenter
                text: qsTr(model.auction.bidprice)
                font.pixelSize: 14
                font.family: "Calibri"
            }

            Rectangle {
                id: bid
                x: 83
                y: 209
                width: 70
                height: 23
                Text {
                    id: text8
                    x: 0
                    y: 0
                    width: 70
                    height: 20
                    text: qsTr("Bid")
                    horizontalAlignment :Text.AlignHCenter
                    verticalAlignment :Text.AlignVCenter
                    font.pixelSize: 14
                    font.bold : true
                    font.family: "Calibri"
                }
            }
            MouseArea {
                        anchors.fill: parent
                        onClicked: { controller.auctionSelected(model.auction) }
            }
        }
        add: Transition {
            NumberAnimation { property: "opacity"; from: 0; to: 1.0; duration: 500 }
            NumberAnimation { property: "scale"; easing.type: Easing.OutBounce; from: 0; to: 1.0; duration: 750 }
        }

        addDisplaced: Transition {
            NumberAnimation { properties: "y"; duration: 600; easing.type: Easing.InBack }
        }

        remove: Transition {
            NumberAnimation { property: "scale"; from: 1.0; to: 0; duration: 200 }
            NumberAnimation { property: "opacity"; from: 1.0; to: 0; duration: 200 }
        }

        removeDisplaced: Transition {
            NumberAnimation { properties: "x,y"; duration: 500; easing.type: Easing.OutBack }
        }
    }

    ListView {
        id: pythonList2
        x:20
        y:270
        width:920
        height:260
        spacing: 20

        model: pythonListModel2
        orientation: Qt.Horizontal

        delegate: Rectangle {
            id: button4
            width: 160
            height: 240
            color:"#D5D5D5"

            Image {
                id: image2
                x: 0
                y: 0
                width: 160
                height: 160
                fillMode: Image.PreserveAspectFit
                smooth: true
                source: model.auction.thumbnailpath
            }

            Text {
                    id: text4
                    x: 0
                    y: 177
                    width: 160
                    height: 26
                    text: qsTr(model.auction.name)
                    font.pixelSize: 12
                }

            Rectangle {
                id: button5
                x: 8
                y: 209
                width: 69
                height: 23
                Text {
                                id: text5
                                x: 0
                                y: 0
                                width: 160
                                height: 26
                                text: qsTr(model.auction.buyoutprice)
                                font.pixelSize: 12
                            }
            }

            Rectangle {
                id: button6
                x: 83
                y: 209
                width: 69
                height: 23
                Text {
                                id: text6
                                x: 0
                                y: 0
                                width: 160
                                height: 26
                                text: qsTr(model.auction.bidprice)
                                font.pixelSize: 12
                            }
            }
            MouseArea {
                        anchors.fill: parent
                        onClicked: { controller.auctionSelected(model.auction) }
            }
        }
    }
}