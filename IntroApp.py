from direct.showbase.ShowBase import ShowBase
 

class MyApp(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)

        # Load the environment model.
        self.environ = self.loader.loadModel("models/environment")
        # self.environ is now a NodePath, or a handler for the node (the actual model)
        # could load the same model several times with different NodePaths
        print('NodePath', self.environ)
        print('Node', self.environ.node())
        # Reparent the NodePath to render, so the engine knows to show it in the scene.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the NodePath.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)
 		
if __name__ == "__main__":
	app = MyApp()
	app.run()