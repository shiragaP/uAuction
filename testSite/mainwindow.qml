import QtQuick 2.0

ListView {
    anchors.fill: parent
    id: list
    spacing: 1
    model: ListModel {
        ListElement { imagePath: "http://uAuction.mooo.com:8080/Users/Waterstrider/PycharmProjects/uAuction/resources/img/logo.png";}
        ListElement { imagePath: "UP10631108H05_788C087B3445FED333D2_L.png"}
        ListElement { imagePath: "noimage.png";}
        ListElement { imagePath: "UP10631108H05_788C087B3445FED333D2_L.png"}
        ListElement { imagePath: "noimage.png";}
        ListElement { imagePath: "UP10631108H05_788C087B3445FED333D2_L.png"}
        ListElement { imagePath: "noimage.png";}
        ListElement { imagePath: "UP10631108H05_788C087B3445FED333D2_L.png"}
        ListElement { imagePath: "noimage.png";}
        ListElement { imagePath: "UP10631108H05_788C087B3445FED333D2_L.png"}
        ListElement { imagePath: "noimage.png";}
        ListElement { imagePath: "UP10631108H05_788C087B3445FED333D2_L.png"}

    }
    orientation: Qt.Horizontal

    delegate: Rectangle {
        id: itemDelegate
        property int listX: x-list.contentX
        property real angleZ: -35 + (90 * listX)  / list.width       // 0 - 90 degrees
        transform: Rotation { origin.y: height / 2; origin.x: 150; axis { x: 0; y: 1; z: 0 } angle: angleZ}
        width: 300
        height: parent.height
        border.color: "lightgray"
        color: "red"
        Image {
            id: imageItem
            height: parent.height; width: parent.width
            anchors.left: parent.left
            fillMode: Image.PreserveAspectFit
            smooth: true
            // deligate can directly ues ListElement role name
            source: imagePath
        }
        /*
        Binding {
            target: itemDelegate
            property: "angleZ"
            value: 0
            when: !(list.moving || list.dragging)
        }

        Behavior on angleZ {
            NumberAnimation {duration: 200; to: 0}
            enabled: !(list.flicking || list.dragging)
        }
        */
    }
}