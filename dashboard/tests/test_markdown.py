import CommonMark
from django.test import TestCase


class TestCommonMark(TestCase):
    def setUp(self):
        self.parser = CommonMark.Parser()
        self.renderer = CommonMark.HtmlRenderer(options={'safe': True})

    def testEmphasis(self):
        ast = self.parser.parse("Hello *World*")
        html = self.renderer.render(ast)

        self.assertEqual(html, u'<p>Hello <em>World</em></p>\n')

    def testInlineHtml(self):
        ast = self.parser.parse("Hello <a href=\"abc\">*World*</a>")
        html = self.renderer.render(ast)

        if ('href' in html):
            self.assertTrue('href' not in html)

    def testXssJavascript(self):
        ast = self.parser.parse("[Click me!](javascript:alert('xss'))")
        html = self.renderer.render(ast)

        if ('href' in html):
            self.assertTrue('javascript' not in html)
