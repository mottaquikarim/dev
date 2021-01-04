# Definitions
ROOT                    := $(PWD)
SITEROOT                := blog
SITEPATH                := ${PWD}/${SITEROOT}
POSTSPATH               := posts
PORT                    := 1313

#   Format according to gofmt: https://github.com/cytopia/docker-gofmt
#   Usage:
#       make new path=my_awesome_blog
new:
ifndef path
	$(eval PATH=${SITEROOT})
else
	$(eval PATH=${path})
endif
	docker run --rm -it -v ${ROOT}:/src -u hugo jguyomard/hugo-builder hugo new site ${PATH}

# TODO: dockerize!
add-theme:
ifndef theme
	$(error theme is required)
endif
ifndef theme_name
	$(error theme_name is required)
endif
	git init
	git submodule add ${theme} ${SITEPATH}/themes/${theme_name}
	echo 'theme = "${theme_name}"' >> ${SITEPATH}/themes/config.toml

new-post:
ifndef post_slug
	$(error post_slug is required (ex: my-awesome-post))
endif
	docker run --rm -it -v ${SITEPATH}:/src -u hugo jguyomard/hugo-builder hugo new ${POSTSPATH}/${post_slug}.md

new-page:
ifndef page_name
	$(error page_name is required (ex: about))
endif
	docker run --rm -it -v ${SITEPATH}:/src -u hugo jguyomard/hugo-builder hugo new ${page_name}/index.md

build:
	docker run --rm -it -v ${SITEPATH}:/src -u hugo jguyomard/hugo-builder hugo

develop:
	docker run \
		--rm -it -d \
		-v ${SITEPATH}:/src \
		-p ${PORT}:1313 \
		-u hugo \
		jguyomard/hugo-builder hugo server -w --bind=0.0.0.0

