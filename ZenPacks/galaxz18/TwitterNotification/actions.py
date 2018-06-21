import logging

from zope.component import adapts
from zope.interface import implements

from Products.ZenModel.actions import IActionBase
from Products.ZenModel.interfaces import IAction
from Products.ZenModel.NotificationSubscription import NotificationSubscription
from Products.Zuul.form import schema
from Products.Zuul.infos import InfoBase
from Products.Zuul.infos.actions import ActionFieldProperty
from Products.Zuul.interfaces import IInfo
from Products.Zuul.utils import ZuulMessageFactory as _t


LOG = logging.getLogger("zen.TwitterNotificaiton")


class ITwitterActionContentInfo(IInfo):
    consumer_key = schema.TextLine(
        title=_t(u"Consumer Key"),
        description=_t(u"Twitter application consumer key."))

    consumer_secret = schema.TextLine(
        title=_t(u"Consumer Secret"),
        description=_t(u"Twitter application consumer secret."))

    access_token_key = schema.TextLine(
        title=_t(u"Access Token Key"),
        description=_t(u"Twitter application access token key."))

    access_token_secret = schema.TextLine(
        title=_t(u"Access Token Secret"),
        description=_t(u"Twitter application access token secret."))


class TwitterActionContentInfo(InfoBase):
    implements(ITwitterActionContentInfo)
    adapts(NotificationSubscription)

    consumer_key = ActionFieldProperty(ITwitterActionContentInfo, "consumer_key")
    consumer_secret = ActionFieldProperty(ITwitterActionContentInfo, "consumer_secret")
    access_token_key = ActionFieldProperty(ITwitterActionContentInfo, "access_token_key")
    access_token_secret = ActionFieldProperty(ITwitterActionContentInfo, "access_token_secret")


class TwitterAction(IActionBase):
    implements(IAction)

    id = "twitter"
    name = "Twitter"
    actionContentInfo = ITwitterActionContentInfo

    shouldExecuteInBatch = False

    def setupAction(self, dmd):
        pass

    def execute(self, notification, signal):
        try:
            import twitter
        except ImportError:
            LOG.error("python-twitter is not installed")
            return

        api = twitter.Api(
            consumer_key=notification.content.get("consumer_key"),
            consumer_secret=notification.content.get("consumer_secret"),
            access_token_key=notification.content.get("access_token_key"),
            access_token_secret=notification.content.get("access_token_secret"))

        try:
            api.PostUpdate(signal.message)
        except Exception as e:
            LOG.error("%s", e)
            return
