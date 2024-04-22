window.components = {
    myComponent: {
        template: `
    <div class="test" ng-controller="ctrl-my-component as ctrl">
        <div class="test">
            TEST TEST
            <div class="test2">TEST TEST2</div>
        </div>
        <div class="test test3">
            TEST TEST3
            <div class="test4">TEST {{ ctrl.message }}</div>
        </div>
        <div id="test">TEST TEST</div>
    </div>
`,
        controllerName: "ctrl-my-component",
        controller: function () {
            this.message = 'test';
        }
    },
    myComponent2: {
        template: `
    <div class="test" ng-controller="ctrl-my-component2 as ctrl">
        <div class="test">
            TEST TEST
            <div class="test2">TEST TEST2</div>
        </div>
        <div class="test test3">
            TEST TEST3
            <div class="test4">TEST {{ ctrl.message }}</div>
        </div>
        <div id="test">TEST TEST</div>
    </div>
`,
        controllerName: "ctrl-my-component2",
        controller: function () {
            this.message = 'test';
        }
    },
};