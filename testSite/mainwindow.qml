import QtQuick 2.0

ListView {
    anchors.fill: parent
    id: list
    spacing: 10
    model: 100

    delegate: Rectangle {
        id: itemDelegate
        property int listY: y - list.contentY
        property real angleZ: (90 * listY)  / list.height       // 0 - 90 degrees
        transform: Rotation { origin.x: width / 2; origin.y: 30; axis { x: 1; y: 0; z: 0 } angle: angleZ}
        //transform: Rotation { origin.x: 0; origin.y: 30; axis { x: 1; y: 1; z: 0 } angle: angleZ}     <--- I like this one more!
        width: parent.width
        height: 50
        border.color: "lightgray"
        color: "red"

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
    }
}