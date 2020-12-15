from api import create_app
import api.config


if __name__ == "__main__":
    app = create_app(api.config.DevelopmentConf)
    app.run()
