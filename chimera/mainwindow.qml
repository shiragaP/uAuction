import QtQuick 2.0
Rectangle {
    id: button0
    width:920
    height:520
    ListView {
    id: pythonList
    x:20
    y:10
    width:920
    height:260
    spacing: 20

    model: pythonListModel1
    orientation: Qt.Horizontal

    delegate: Rectangle {
        id: button1
        width: 160
        height: 240
        color:"#D5D5D5"

        Image {
            id: image1
            x: 0
            y: 0
            width: 160
            height: 176
            fillMode: Image.PreserveAspectFit
            smooth: true
            source: model.auction.thumbnailpath
        }

        Text {
                id: text1
                x: 0
                y: 177
                width: 160
                height: 26
                text: qsTr(model.auction.name)
                font.pixelSize: 12
            }

        Rectangle {
            id: button2
            x: 8
            y: 209
            width: 69
            height: 23
            Text {
                            id: text2
                            x: 0
                            y: 0
                            width: 160
                            height: 26
                            text: qsTr(model.auction.buyoutprice)
                            font.pixelSize: 12
                        }
        }

        Rectangle {
            id: button3
            x: 83
            y: 209
            width: 69
            height: 23
            Text {
                            id: text3
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
            height: 176
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