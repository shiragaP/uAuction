import QtQuick 2.0

Rectangle {
    id: homeScreen
    objectName: "homeScreen"
    width: 1366
    height: 768
    color: "#f0f0f0"
    property string usertype: ""

    Rectangle {
        id: actionBar
        objectName: "actionBar"
        x: 0
        y: 0
        width: 1366
        height: 150
        color: "#940009"

        Image {
            id: image1
            x: 30
            y: 15
            width: 146
            height: 121
            source: "res/home-screen/logo.png"
            sourceSize.height: 121
            sourceSize.width: 146
        }

        Image {
            id: image2
            x: 198
            y: 57
            width: 228
            height: 79
            source: "res/home-screen/title.png"
            sourceSize.height: 79
            sourceSize.width: 228
        }

        Rectangle {
            id: rectangle1
            x: 492
            y: 57
            width: 700
            height: 70
            color: "#ffffff"
            radius: 10
            border.width: 3
            border.color: "#aeaeae"

            TextInput {
                id: searchInput
                color: "#5c5c5c"
                text: qsTr("Search for restaurants, foods, and things")
                font.bold: false
                font.family: "Tahoma"
                anchors.rightMargin: 70
                anchors.leftMargin: 20
                anchors.bottomMargin: 15
                anchors.topMargin: 15
                anchors.fill: parent
                font.pixelSize: 26
                verticalAlignment: Text.AlignVCenter
                onFocusChanged: {
                    if (searchInput.text === "Search for restaurants, foods, and things") {
                        searchInput.text = ""
                    }
                }
            }

            Image {
                id: image3
                x: 640
                y: 14
                width: 41
                height: 42
                anchors.rightMargin: 20
                anchors.right: parent.right
                source: "res/home-screen/search.png"
            }
        }

    }

    Rectangle {
        id: view
        x: 83
        y: 208
        width: 1200
        height: 490
        color: "#00000000"
        border.width: 0
        border.color: "#000000"

        ListView  {
            id: listView
            x: 0
            y: 0
            width: 1200
            height: 490
            spacing: -200
            orientation: ListView.Horizontal
            preferredHighlightBegin: view.width / 6
            preferredHighlightEnd: view.width / 6
            focus: true
            Keys.onTabPressed: incrementCurrentIndex()
            highlightRangeMode: ListView.StrictlyEnforceRange
            highlightMoveVelocity: 1000
            property ListModel items: ListModel {}

            model: wrapper.restaurants

            delegate: Image {
                id: itemDelegate
                property int listX: x - listView.contentX
                property real angleZ: 50
                property real side: 0
                transform: Rotation { origin.x: width / 2; origin.y: height / 2; axis { x: 0; y: side; z: 0 } angle: angleZ}
                width: 820
                height: 460
                source: model.object.path

                Rectangle {
                    id: nameBar
                    width: parent.width
                    height: 70
                    anchors.bottom: parent.bottom
                    color: "#000000"
                    opacity: 0.7
                    visible: true

                }

                Text {
                    id: name
                    anchors.fill: nameBar
                    text: model.object.name
                    font.bold: true
                    font.family: "Tahoma"
                    color: "#ffffff"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    opacity: 1
                    font.pixelSize: 40
                }

                Binding {
                    target: itemDelegate
                    property: "side"
                    value: 0
                    when: index == listView.currentIndex
                }

                Binding {
                    target: itemDelegate
                    property: "side"
                    value: 1
                    when: index < listView.currentIndex
                }

                Binding {
                    target: itemDelegate
                    property: "side"
                    value: -1
                    when: index > listView.currentIndex
                }

                Binding {
                    target: itemDelegate
                    property: "angleZ"
                    value: 0
                    when: index == listView.currentIndex
                }

                Binding {
                    target: itemDelegate
                    property: "angleZ"
                    value: 50
                    when: !(index == listView.currentIndex)
                }

                Binding {
                    target: itemDelegate
                    property: "scale"
                    value: 1
                    when: index == listView.currentIndex
                }

                Binding {
                    target: itemDelegate
                    property: "scale"
                    value: 0.8
                    when: !(index == listView.currentIndex)
                }

                Behavior on scale {
                    NumberAnimation { duration: 400; easing.type: Easing.OutSine}
                }

                Behavior on side {
                    NumberAnimation { duration: 400;}
                }

                Behavior on angleZ {
                    NumberAnimation {duration: 400; easing.type: Easing.OutSine}
                }

                MouseArea {
                    id: itemDelegateArea
                    anchors.fill: itemDelegate
                    onClicked: { linksys.print(model.object.name); wrapper.add() }
                }
            }
        }
    }
}
