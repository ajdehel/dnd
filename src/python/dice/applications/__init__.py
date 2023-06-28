class Application:

    @classmethod
    def Run(cls):
        try:
            args = cls.Parser.parse_args()
            app = cls(args)
            app()
        except KeyboardInterrupt:
            pass
