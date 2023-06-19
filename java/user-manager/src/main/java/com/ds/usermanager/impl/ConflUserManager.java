package com.ds.usermanager.impl;

import java.io.IOException;
import java.util.Optional;

import javax.servlet.annotation.MultipartConfig;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.beans.factory.annotation.Autowired;

import com.atlassian.confluence.api.model.content.Space;
import com.atlassian.confluence.api.service.content.SpaceService;
import com.atlassian.templaterenderer.RenderingException;
import com.atlassian.templaterenderer.TemplateRenderer;
import com.atlassian.user.UserManager;
import com.atlassian.plugin.spring.scanner.annotation.component.BambooComponent;
import com.atlassian.plugin.spring.scanner.annotation.imports.ComponentImport;
import com.google.common.collect.ImmutableMap;

import static java.util.Objects.requireNonNull;

@BambooComponent
@MultipartConfig
@SuppressWarnings("serial")
@WebServlet("/cumanager")
public class ConflUserManager extends HttpServlet {
	
	@ComponentImport
	@Autowired
	private final UserManager userManager;
	@ComponentImport
	@Autowired
	private final SpaceService spaceService;	
	@ComponentImport
	@Autowired
	private final TemplateRenderer templateRenderer;	
	
	@Autowired
	public ConflUserManager(UserManager userManager, SpaceService spaceService, TemplateRenderer templateRenderer) {
		this.userManager = requireNonNull(userManager);
		this.spaceService = requireNonNull(spaceService);
		this.templateRenderer = requireNonNull(templateRenderer);
	}
	
	@Override
	protected void doGet(HttpServletRequest request, HttpServletResponse response) {
		
		Space space = null;
				
		space = getCurrentSpace(request);
		
		
		try {
			response.setContentType("text/html;charset=utf-8");
			templateRenderer.render("template/umanager.vm", 
					ImmutableMap.of("spaceId", space.getId()), 
					response.getWriter());
		} catch (RenderingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
	
	private Space getCurrentSpace(HttpServletRequest request) {
		Space space = null;
		String spaceKey = request.getParameter("key");
		if (spaceKey != null && !spaceKey.equals("")) {
			Optional<Space> searchResults = spaceService.find().withKeys(spaceKey).fetch();
			if (searchResults.isPresent()) {
				space = searchResults.get();
			}
			else {
				space = null;
			}
		}
		return space;
	}

}