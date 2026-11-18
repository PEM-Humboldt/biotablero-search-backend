from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "polygon_metric_item" RENAME TO "polygon_metric_layer";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "polygon_metric_layer" RENAME TO "polygon_metric_item";"""


MODELS_STATE = (
    "eJztXW1v2zYQ/iuGP61AVjRZkxbDMMBx3NVrEgeJuxUNAoGWaFuILKp6SWIU+e8j9UpJlC"
    "x5siNG9ykJdSdRj8i7545H5md/5ioORra6VGb3bwc2RtO1hfu/9372TbRivxRIHPT6yLKy"
    "11mzi2aGr4iorOJGwjPHtZHq0gtzZDiYNmnYUW3dcnVi0lbTMwzWSFQqqJuLpMkz9R8eVl"
    "yywO4S2/TC7R1t1k0NP2En+tO6V+Y6NrRU33WNPdtvD3pC24ZLZH/yJdnjZopKDG9lJtLW"
    "2l0SMxanvWGtC2xiG7lY416A9S982agp6CttcG0Px53UkgYNz5FnuNwLV0RBJSZDUDddx3"
    "/FFXpSDGwu3CX98/jdc/AyyasGUuwN/hlcDz8Prn85fvem/+zLIRcFkj56CVz0bbBRB7FY"
    "QUbQjo6PK6BGpQLYEpg8S2MvpSA3j9UZveLqKyzGK62ZAU0LVd9Gv2wDYdSQYJhMt4ZApN"
    "Nam5jGOvw+JRhOxxejm+ng4oq9ycpxfhg+RIPpiF058lvXmdZfTt6wdkKNRWBG4pv0/h1P"
    "P/fYn73vk8uRjyBx3IXtPzGRm37vsz4hzyWKSR4VpHFDKWqNOs9Mx/yemw2sYYbU+0dka0"
    "rqSjIALGKsFxSV/Oc/DTU/fbnGBvKhzX/olEW9Cu7Vzm/9HA3gqJWHjRyRItzyl1ZHq2wL"
    "MtHC7zV7NntSCpchMQyshh0u8EacTAV/pKalW+OQxqZbwx+xj5AZK+HQflHLumBP+fXo8P"
    "2H9x9/O3n/kYr4PYlbPpTYifHldINn8n/WcEyRvIx+6fBdFW9OpbJ+CRkGeXQUA62xLTBN"
    "hBgYmWK8sqpZi0V1d2Wh6s4+sYkSQXU6mZynPM/peJr2LZdfL05HFEvf5VAh3cX8eASXDy"
    "4/psZ0Zih0fKwa8fqJ5zqPplz7Pnuh9+dnxgrTm6iNgHLh3yrt1CVCZZ+cKBg1FYhRPLyq"
    "s6PECwBHkokjPSDDE5CkQuhi+c3otWPmNQNg1qZ7ds2UB6fUDL3cA3LNJD5mM/KUx+rvm8"
    "mlGKtIPgPTV5N2/1bTVfegZ+iOe7cr0Pp/zD3Tt2m9macbrm46b9kD/+zvhG8yIFK05zLC"
    "8mLwLUNxLofnk9Msn2E3OAXm+WqZJ/9dOX9by+Hl9LpkvXPUXYRnHsxPxMb6wvyC1z6mY9"
    "ovZKoi31eSXmofokVMlDbb6DFmVvkhQ3/RsIGDYHc4uBkOzkb95+IwaPfM9uxq2C9ks+xi"
    "BQarWSqQVtlIa/jRMvPVIKgAulA+g92cKbR6korQOZt8PT0f9a6uR8PxzTjkDrGL8i+m81"
    "LXo8F5hh5YqJ77iOW75DYygNVNJnMqchL+w0rrw4fHuYyySl9qQex1HbR4nY7BBVz9dXL1"
    "cL23pqVNKXXJ3JawdCtZ7W6Eoku5ep7l5+mR0j5yHuTl+4X8PLxegaKvEklg6S2btWUsHZ"
    "bfKyy/E4u9lR69bw248pqSEqf/Wblg+iAgQT6+SvECrw31C8BMu8BMKWY6DbiIrajM2des"
    "dxYpb2V5wp6+mOE5qWJ3Tnyzs1X1R5JBhUKHggHYHC5j/pbSwjInTSIS3E1SMKL4psFSoT"
    "DuSyIPSaEJIGmuriyFi4ylZfuKZquUl4vMdLUIV4Fac3mDXd1RLFtfIVHauzQOSSvuMQTZ"
    "2QpVgxHIwiaeVXvpJa0lJTfdOiiGmO11xmxQ+bOVwc6TpjrgpXS6BFzJYkySjW9kLUZGMn"
    "6QWYpJDRPxSox4KjeGoqxZgSySEhSdZdMNGwKBVF6iYhyQSo9AGNA241gaBhRntiqkVDu3"
    "+rVEjuKz9ZpBU0oPlm0gBOhCCAAMFhjsyzHYNnCuOdlMt4JFj8pMKxQHktWy+VtGsupWyn"
    "S0PoZ/eg6tKX4q2iyRVpMFtDI/P/o2Tbn43BbL2M2fTy7/isSz+y6BZQHLApYFLOu1sqyo"
    "LL6QYnF185v4FVeyv1NudctSAcv+HXCshjmWD2sNjhXJN7LaKsmRngtM2JQWrPgXn27B67"
    "zUCRc7I1o7Octir9sIXnrdf+uxyM5NFjjb4j3RkQJsio52Ysznuqojg2Kk1duIkVWU0AZC"
    "vQmEQTl74r9Bze0BWT1Z0gdbH41eEgKlzrJvJAriT9JvH4ZV46DsGKkbCm04CKR+AXR4Vo"
    "w8iAoyFlAhDxXyFXdW2MRlIoKs8BbI0JsNw3tJiodjYVXHjkJNsNvIaLkJbngT3U8iXPaW"
    "Zdp0PEDOElXMOCm7Oi3gls9pJQ/has3vYN1vtzkp/+xZwQwtzrYkGpBrqZJrebH9Flth23"
    "eJG+zchxgYYmBYCnxhww1HX8HRV3vJH1Q5+io/j2EpWrqlaD7erhYpVP7PFelwYVf/veKW"
    "G3vcVGZ5iRB71UCOw36H6GHH0UOMdA1my+vImcnemtRyY7TyPpZEpWNgwT8FqblcDSEThE"
    "wQMkHIBIWnLWH7grEIQadM5y3HC3HFgRK3VLcxPOLXCGF3VNvM30FJnMM+nWDqFlcCRgpQ"
    "CRiRU7M2hokKoLi5zGDDYIy1AEseS8/cDs1ED/CE8PNVh58QRcHCU4djgFThWWEckC1P2x"
    "QL5OrjIB5o20Q+KIkH5KrpaUU6P64rqjjaYvkuOY8UYEtKKVz6mlS0LnYCVYBRUQUnyFXB"
    "UBUdItdFALGAu1QBEIsipS4C+OBtB2Cg11UAdfMBOfqDwNcWcxVOpauwYdrTlWjVphA1Tq"
    "PjoCnJ5KuPX0a5q1BCQggSQpAQgoTQK0sIDbCtq8t+YSoovH6wOQmEEknI/rRs1h6UZH8e"
    "sO0ID4AsTv1wKnLmfbY/RMcSHERectaFJTp/XBKQtk6O0btSuijgScXbMDkV2IeZJTnRPs"
    "yc792n43j+D04BHKM="
)
