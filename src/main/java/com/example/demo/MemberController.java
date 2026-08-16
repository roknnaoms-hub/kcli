package com.example.demo;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import lombok.RequiredArgsConstructor;

@Controller
@RequiredArgsConstructor
@RequestMapping("/members")
public class MemberController {
    private final MemberService memberService;

    @GetMapping
    public String list(Model model) {
        model.addAttribute("members", memberService.findAll());
        return "members/list";
    }

    @GetMapping("/new")
    public String createForm(Model model) {
        model.addAttribute("member", new Member());
        return "members/createForm";
    }

    @PostMapping
    public String create(@ModelAttribute Member member) {
        memberService.save(member);
        return "redirect:/members";
    }
}